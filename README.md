(this is made with google jules and ai because I have no idea how to use ollama.)

# OllamaHost: Multi-Agent API Server

OllamaHost has evolved! It's now a powerful multi-agent API server that lets you create, manage, and interact with multiple, stateful Ollama agents. Each agent has its own persistent conversation memory, allowing for complex, ongoing dialogues.

The server uses `ngrok` to generate a secure, public URL, so you can access your agents from anywhere.

## Features

-   **Multi-Agent Management**: Create and delete agents on the fly via API commands.
-   **Persistent Memory**: Each agent has its own conversation history that is saved to disk, so you can stop and restart the server without losing context.
-   **Stateful Conversations**: The API automatically includes an agent's history in every new request, enabling true conversational AI.
-   **Secure Access**: The entire agent management API is protected by a single master key.
-   **Publicly Accessible**: Generates a random, public URL on every run, making it easy to integrate with other services or use from any device.

## Quick Start

1.  **Install Ollama**:
    -   If you haven't already, download and install Ollama from [ollama.com/download](https://ollama.com/download).

2.  **Run the Start Script**:
    -   Open your terminal and run the `Start.py` script:
        ```bash
        python3 Start.py
        ```
    -   The script will install all dependencies, start the server, and generate your public URL and master key.

3.  **Get Your Credentials**:
    -   The script will print your unique public URL and master key to the console. It will look like this:
        ```
        ✅ Your Ollama API is now publicly accessible!
        ============================================================
        Use this URL to send requests from anywhere:

        https://<random-string>.ngrok-free.app

        Your Master Key is: <your_master_key>
        ```
    -   **Important**: You will need both the **Public URL** and the **Master Key** to use the API.

## API Reference

Here are the available commands. Replace `YOUR_PUBLIC_URL` and `YOUR_MASTER_KEY` with the values from your terminal.

---

### 1. Create an Agent

Creates a new agent with a unique name and a specified Ollama model.

-   **Endpoint**: `POST /agents/create`
-   **Body**: `{"agent_name": "MyAssistant", "model": "llama3"}`

**cURL**
```bash
curl -X POST "YOUR_PUBLIC_URL/agents/create?key=YOUR_MASTER_KEY" \
     -H "Content-Type: application/json" \
     -d '{"agent_name": "MyAssistant", "model": "llama3"}'
```

**Python**
```python
import requests

url = "YOUR_PUBLIC_URL/agents/create?key=YOUR_MASTER_KEY"
payload = {"agent_name": "MyAssistant", "model": "llama3"}
response = requests.post(url, json=payload)
print(response.json())
```

**JavaScript (Node.js)**
```javascript
fetch('YOUR_PUBLIC_URL/agents/create?key=YOUR_MASTER_KEY', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ agent_name: 'MyAssistant', model: 'llama3' })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

### 2. Generate a Response

Have a conversation with an agent. The history is managed automatically.

-   **Endpoint**: `POST /agents/{agent_name}/generate`
-   **Body**: `{"prompt": "Hello, what is the capital of France?"}`

**cURL**
```bash
curl -X POST "YOUR_PUBLIC_URL/agents/MyAssistant/generate?key=YOUR_MASTER_KEY" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, what is the capital of France?"}'
```

**Python**
```python
import requests

url = "YOUR_PUBLIC_URL/agents/MyAssistant/generate?key=YOUR_MASTER_KEY"
payload = {"prompt": "Hello, what is the capital of France?"}
response = requests.post(url, json=payload)
print(response.json()['message']['content'])
```

**JavaScript (Node.js)**
```javascript
fetch('YOUR_PUBLIC_URL/agents/MyAssistant/generate?key=YOUR_MASTER_KEY', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: 'Hello, what is the capital of France?' })
})
.then(res => res.json())
.then(data => console.log(data.message.content));
```

---

### 3. View Agent Memory

Retrieve the full conversation history for an agent.

-   **Endpoint**: `GET /agents/{agent_name}/memory`

**cURL**
```bash
curl "YOUR_PUBLIC_URL/agents/MyAssistant/memory?key=YOUR_MASTER_KEY"
```

**Python**
```python
import requests

url = "YOUR_PUBLIC_URL/agents/MyAssistant/memory?key=YOUR_MASTER_KEY"
response = requests.get(url)
print(response.json())
```

**JavaScript (Node.js)**
```javascript
fetch('YOUR_PUBLIC_URL/agents/MyAssistant/memory?key=YOUR_MASTER_KEY')
.then(res => res.json())
.then(data => console.log(data));
```

---

### 4. Edit Agent Memory

Manually overwrite an agent's memory. This is useful for correcting mistakes or guiding the agent's future responses.

-   **Endpoint**: `POST /agents/{agent_name}/memory/edit`
-   **Body**: `{"new_memory": [{"user": "...", "assistant": "..."}]}`

**cURL**
```bash
curl -X POST "YOUR_PUBLIC_URL/agents/MyAssistant/memory/edit?key=YOUR_MASTER_KEY" \
     -H "Content-Type: application/json" \
     -d '{"new_memory": [{"user": "The capital of France is Lyon.", "assistant": "You are incorrect. The capital is Paris."}]}'
```

**Python**
```python
import requests

url = "YOUR_PUBLIC_URL/agents/MyAssistant/memory/edit?key=YOUR_MASTER_KEY"
payload = {
    "new_memory": [
        {"user": "The capital of France is Lyon.", "assistant": "You are incorrect. The capital is Paris."}
    ]
}
response = requests.post(url, json=payload)
print(response.json())
```

**JavaScript (Node.js)**
```javascript
const newMemory = [
  { user: 'The capital of France is Lyon.', assistant: 'You are incorrect. The capital is Paris.' }
];
fetch('YOUR_PUBLIC_URL/agents/MyAssistant/memory/edit?key=YOUR_MASTER_KEY', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ new_memory: newMemory })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

### 5. Delete an Agent

Permanently deletes an agent and its conversation history.

-   **Endpoint**: `POST /agents/delete`
-   **Body**: `{"agent_name": "MyAssistant"}`

**cURL**
```bash
curl -X POST "YOUR_PUBLIC_URL/agents/delete?key=YOUR_MASTER_KEY" \
     -H "Content-Type: application/json" \
     -d '{"agent_name": "MyAssistant"}'
```

**Python**
```python
import requests

url = "YOUR_PUBLIC_URL/agents/delete?key=YOUR_MASTER_KEY"
payload = {"agent_name": "MyAssistant"}
response = requests.post(url, json=payload)
print(response.json())
```

**JavaScript (Node.js)**
```javascript
fetch('YOUR_PUBLIC_URL/agents/delete?key=YOUR_MASTER_KEY', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ agent_name: 'MyAssistant' })
})
.then(res => res.json())
.then(data => console.log(data));
```
