from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter
from fastapi.responses import Response, JSONResponse
import secrets
import os
import requests

PASSWORD_FILE = "password.txt"
OLLAMA_API_URL = "http://localhost:11434"

# This will be populated at startup
PASSWORD = None

# --- Main App ---
app = FastAPI(title="OllamaHost API", description="Host your local Ollama LLMs and access via a password-protected URL.")

def get_password():
    """Generate or load password from file."""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            return f.read().strip()
    password = secrets.token_urlsafe(16)
    with open(PASSWORD_FILE, "w") as f:
        f.write(password)
    return password

@app.on_event("startup")
async def startup_event():
    """On startup, generate or load the password."""
    global PASSWORD
    PASSWORD = get_password()

# --- Dependency for password verification ---
def verify_password_query(password: str = None):
    if password is None:
        raise HTTPException(status_code=401, detail="Password required as a query parameter.")
    if not secrets.compare_digest(password, PASSWORD):
        raise HTTPException(status_code=401, detail="Invalid password.")

# --- Proxy Router ---
proxy_router = APIRouter(dependencies=[Depends(verify_password_query)])

@proxy_router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_to_ollama(full_path: str, request: Request):
    method = request.method
    url = f"{OLLAMA_API_URL}/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)

    query_params = dict(request.query_params)
    query_params.pop("password", None)

    body = await request.body()

    try:
        resp = requests.request(method, url, headers=headers, data=body, params=query_params, stream=True)
        return Response(content=resp.raw.read(), status_code=resp.status_code, headers=dict(resp.headers))
    except requests.exceptions.ConnectionError as e:
        return JSONResponse(status_code=502, content={"error": "Failed to connect to Ollama API. Is Ollama running?", "details": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "An unexpected error occurred", "details": str(e)})

# --- Public Root Endpoint ---
@app.get("/")
def root(request: Request):
    proxy_access_url = f"{request.base_url}proxy/api/generate?password={PASSWORD}"
    return {
        "message": "OllamaHost API is running. Use the access URL to send requests to the proxy.",
        "access_url": proxy_access_url,
        "ollama_api_docs": "https://github.com/ollama/ollama/blob/main/docs/api.md"
    }

# Include the proxy router in the main app
app.include_router(proxy_router, prefix="/proxy")