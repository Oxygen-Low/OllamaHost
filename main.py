from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import secrets
import os
import requests

from agents import agent_manager

KEY_FILE = "key.txt"
OLLAMA_API_URL = "http://localhost:11434"

# This will be populated at startup
KEY = None

# --- Main App ---
app = FastAPI(
    title="OllamaHost Multi-Agent API",
    description="Create and manage multiple Ollama agents, each with their own persistent memory."
)

# --- Key Management ---
def get_key():
    """Generate or load key from file."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    key = secrets.token_urlsafe(16)
    with open(KEY_FILE, "w") as f:
        f.write(key)
    return key

@app.on_event("startup")
async def startup_event():
    """On startup, generate or load the key and ensure the agents directory exists."""
    global KEY
    KEY = get_key()
    os.makedirs(agent_manager.AGENTS_DIR, exist_ok=True)

# --- Dependency for key verification ---
def verify_key_query(key: str = None):
    if key is None:
        raise HTTPException(status_code=401, detail="A master 'key' is required as a query parameter.")
    if not secrets.compare_digest(key, KEY):
        raise HTTPException(status_code=403, detail="Invalid master key.")

# --- API Models ---
class AgentCreateRequest(BaseModel):
    agent_name: str
    model: str

class AgentDeleteRequest(BaseModel):
    agent_name: str

class MemoryEditRequest(BaseModel):
    new_memory: List[Dict[str, str]]

class GenerateRequest(BaseModel):
    prompt: str

# --- Agent Management Router ---
# All endpoints in this router are protected by the master key
agent_router = APIRouter(prefix="/agents", dependencies=[Depends(verify_key_query)])

@agent_router.post("/create", status_code=201)
def create_agent_endpoint(request: AgentCreateRequest):
    try:
        agent = agent_manager.create_agent(request.agent_name, request.model)
        return {"message": f"Agent '{agent['name']}' created successfully.", "agent": agent}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) # 409 Conflict

@agent_router.post("/delete", status_code=200)
def delete_agent_endpoint(request: AgentDeleteRequest):
    try:
        agent_manager.delete_agent(request.agent_name)
        return {"message": f"Agent '{request.agent_name}' deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) # 404 Not Found

@agent_router.get("/{agent_name}/memory")
def get_memory_endpoint(agent_name: str):
    if not agent_manager.agent_exists(agent_name):
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found.")
    memory = agent_manager.get_agent_memory(agent_name)
    return {"agent_name": agent_name, "memory": memory}

@agent_router.post("/{agent_name}/memory/edit")
def edit_memory_endpoint(agent_name: str, request: MemoryEditRequest):
    try:
        agent_manager.edit_agent_memory(agent_name, request.new_memory)
        return {"message": f"Memory for agent '{agent_name}' has been updated."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@agent_router.post("/{agent_name}/generate")
def generate_endpoint(agent_name: str, request: GenerateRequest):
    if not agent_manager.agent_exists(agent_name):
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found.")

    agent_config = agent_manager.get_agent(agent_name)
    model = agent_config.get("model")

    # Load history and prepare messages for Ollama
    history = agent_manager.get_agent_memory(agent_name)
    messages = []
    for entry in history:
        messages.append({"role": "user", "content": entry["user"]})
        messages.append({"role": "assistant", "content": entry["assistant"]})

    # Add the new user prompt
    messages.append({"role": "user", "content": request.prompt})

    # Call Ollama API
    try:
        ollama_payload = {
            "model": model,
            "messages": messages,
            "stream": False # Keep it simple for now
        }
        response = requests.post(f"{OLLAMA_API_URL}/api/chat", json=ollama_payload)
        response.raise_for_status() # Raise an exception for bad status codes

        ollama_data = response.json()
        assistant_response = ollama_data.get("message", {}).get("content")

        if not assistant_response:
            raise HTTPException(status_code=500, detail="Received an empty response from Ollama.")

        # Update agent's memory with the new exchange
        agent_manager.update_agent_memory(agent_name, request.prompt, assistant_response)

        return ollama_data

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="Failed to connect to the Ollama API. Is Ollama running?")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while communicating with Ollama: {e}")

# --- Public Root Endpoint ---
@app.get("/")
def root():
    return {
        "message": "OllamaHost Multi-Agent API is running.",
        "docs_url": "/docs",
        "master_key": KEY # Note: In a real production app, you might not want to expose this here.
    }

# Include the agent router in the main app
app.include_router(agent_router)