# OllamaHost
Host Ollama chatbots so they are accessible to your websites.

# OllamaHost

OllamaHost lets you run a local API server to expose your Ollama LLMs securely via an API key. No sign up or sign in required.

## Features
- Runs locally on your computer
- Generates an API key on first run
- Secures API access with the key
- Forwards requests to your local Ollama LLM

## Setup

1. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
2. Start Ollama (https://ollama.com/download)
3. Run the API server:
	```bash
	uvicorn main:app --reload
	```
4. On first run, your API key will be shown at `/` endpoint and saved in `api_key.txt`.

## Usage
- Send POST requests to `/generate` with your prompt and model name, e.g.:
	```bash
	curl -X POST http://localhost:8000/generate \
		-H "x-api-key: <your_api_key>" \
		-H "Content-Type: application/json" \
		-d '{"model": "llama2", "prompt": "Hello!"}'
	```

## Security
- Keep your API key secret. Anyone with the key can access your local LLM.

## License
See LICENSE.
