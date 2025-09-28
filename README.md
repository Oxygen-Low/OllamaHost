# OllamaHost

OllamaHost lets you run a local API server to expose your Ollama LLMs securely via a **public, shareable URL**. It uses `ngrok` to create a secure tunnel to your local machine, so you can access your models from anywhere.

## Features
- Runs locally on your computer.
- **Generates a public, random URL** on every run.
- Generates a secure password to protect your API.
- Forwards requests from the public URL to your local Ollama LLM.

## Setup

1.  **Install Ollama:**
    - Download and install Ollama from [ollama.com/download](https://ollama.com/download).

2.  **Run the Start Script:**
    - Simply run the `Start.py` script in your terminal:
      ```bash
      python3 Start.py
      ```
    - The script will automatically install the required dependencies (including `pyngrok`) and start the server.

## Usage

1.  **Get Your Public Access URL:**
    - After running the script, it will print a public URL to your console. It will look something like this:
      ```
      ✅ Your Ollama API is now publicly accessible!
      ============================================================
      Use this URL to send requests from anywhere:

      https://<random-string>.ngrok-free.app/proxy/api/generate?password=<your_password>
      ```

2.  **Send API Requests from Anywhere:**
    - Use the generated URL to send requests to your Ollama API from any device with an internet connection.
      ```bash
      curl -X POST "https://<random-string>.ngrok-free.app/proxy/api/generate?password=<your_password>" \
           -H "Content-Type: application/json" \
           -d '{"model": "llama2", "prompt": "Hello!"}'
      ```
    - Replace the example URL with the one generated in your terminal.

3.  **Stop the Server:**
    - To stop the server and close the public connection, simply press `CTRL+C` in the terminal where the script is running.

## Security
- Your API is protected by a randomly generated password.
- The `password.txt` file is created locally for the script to use but is included in `.gitignore` to prevent it from being committed to your repository.

## License
See LICENSE.