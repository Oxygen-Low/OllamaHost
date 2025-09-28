# OllamaHost

OllamaHost lets you run a local API server to expose your Ollama LLMs securely via a password-protected URL. No sign up or sign in required.

## Features
- Runs locally on your computer.
- Generates a secure password on first run.
- Secures API access with the password in the URL.
- Forwards requests to your local Ollama LLM.

## Setup

1.  **Install Ollama:**
    - Download and install Ollama from [ollama.com/download](https://ollama.com/download).

2.  **Run the Start Script:**
    - Simply run the `Start.py` script:
      ```bash
      python3 Start.py
      ```
    - This script will automatically install the required dependencies and start the API server.
    - On the first run, it will generate a `password.txt` file (this file is git-ignored for security).

## Usage

1.  **Get Your Access URL:**
    - When the server starts, it will display a message with your unique access URL, which includes the generated password.
    - You can also find this URL by navigating to `http://localhost:8000` in your browser.

2.  **Send API Requests:**
    - Use the provided access URL to send requests to the Ollama API. For example, to generate a response, send a POST request like this:
      ```bash
      curl -X POST http://localhost:8000/proxy/api/generate?password=<your_password> \
           -H "Content-Type: application/json" \
           -d '{"model": "llama2", "prompt": "Hello!"}'
      ```
    - Replace `<your_password>` with the password from your access URL.

## Security
- The server is protected by a randomly generated password.
- The `password.txt` file is added to `.gitignore` to prevent it from being committed to your repository. Keep this file safe.

## License
See LICENSE.