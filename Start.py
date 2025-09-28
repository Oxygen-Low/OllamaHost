import subprocess
import sys
import os
import time
from pyngrok import ngrok

KEY_FILE = "key.txt"
PORT = 8000

def install_dependencies():
    """Installs dependencies from requirements.txt."""
    print("Installing/updating dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Dependencies are up to date.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def start_local_server():
    """Starts the FastAPI server as a background process."""
    print("Starting local server in the background...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", f"--port={PORT}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return server_process

def get_key_from_file():
    """Waits for key.txt to be created and returns the key."""
    print("Waiting for server to generate key...")
    timeout = 20  # 20 seconds
    start_time = time.time()
    while not os.path.exists(KEY_FILE):
        time.sleep(1)
        if time.time() - start_time > timeout:
            print("\nError: Timed out waiting for the key file.")
            print("The local server might have failed to start.")
            return None
    with open(KEY_FILE, "r") as f:
        return f.read().strip()

def create_public_url():
    """Creates a public URL using ngrok."""
    print("Creating a secure public URL with ngrok...")
    try:
        # You may need to add an ngrok authtoken for longer sessions.
        # ngrok.set_auth_token("YOUR_AUTHTOKEN")
        public_url = ngrok.connect(PORT, "http")
        return public_url
    except Exception as e:
        print(f"\nError creating ngrok tunnel: {e}")
        print("Please ensure ngrok is installed and configured correctly.")
        print("You can get an authtoken from https://dashboard.ngrok.com/get-started/your-authtoken")
        return None

if __name__ == "__main__":
    install_dependencies()

    # Ensure any previous ngrok tunnels are gracefully closed
    ngrok.kill()

    server_proc = start_local_server()

    key = get_key_from_file()
    if not key:
        server_proc.kill()
        sys.exit(1)

    public_url = create_public_url()
    if not public_url:
        server_proc.kill()
        sys.exit(1)

    print("\n" + "="*60)
    print("✅ Your Ollama API is now publicly accessible!")
    print("="*60)
    print(f"Public URL: {public_url.public_url}")
    print(f"Master Key: {key}\n")
    print("Refer to the README.md for API commands.")
    print("Keep this script running to maintain the connection.")
    print("Press CTRL+C to stop the server and close the public URL.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        ngrok.disconnect(public_url.public_url)
        server_proc.kill()
        print("Server and public URL have been stopped.")