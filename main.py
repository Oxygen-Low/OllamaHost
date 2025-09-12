
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response, JSONResponse
import secrets
import os
import requests

API_KEY_FILE = "api_key.txt"
OLLAMA_API_URL = "http://localhost:11434"

app = FastAPI(title="OllamaHost API", description="Host your local Ollama LLMs and access via API key.")

# Generate or load API key
def get_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    key = secrets.token_hex(32)
    with open(API_KEY_FILE, "w") as f:
        f.write(key)
    return key

API_KEY = get_api_key()

def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key.")

@app.get("/")
def root():
    return {"message": "OllamaHost API is running.", "api_key": API_KEY}

# Proxy all requests to Ollama
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(full_path: str, request: Request):
    verify_api_key(request)
    method = request.method
    url = f"{OLLAMA_API_URL}/{full_path}" if full_path else OLLAMA_API_URL
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("x-api-key", None)  # Don't forward our API key
    body = await request.body()
    try:
        resp = requests.request(method, url, headers=headers, data=body, params=dict(request.query_params))
        return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
