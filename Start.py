import subprocess
import sys
import os

def install_dependencies():
    """Installs dependencies from requirements.txt."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def start_server():
    """Starts the FastAPI server."""
    print("Starting API server...")
    try:
        # Running without --reload to avoid issues in this environment
        subprocess.check_call([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    install_dependencies()
    start_server()