import os
import json
from typing import List, Dict, Any

AGENTS_DIR = os.path.dirname(__file__)

def get_agent_config_path(agent_name: str) -> str:
    """Returns the path to the agent's config file."""
    return os.path.join(AGENTS_DIR, f"{agent_name}.json")

def get_agent_memory_path(agent_name: str) -> str:
    """Returns the path to the agent's memory file."""
    return os.path.join(AGENTS_DIR, f"{agent_name}_memory.jsonl")

def agent_exists(agent_name: str) -> bool:
    """Checks if an agent's config file exists."""
    return os.path.exists(get_agent_config_path(agent_name))

def create_agent(agent_name: str, model: str) -> Dict[str, Any]:
    """Creates a new agent configuration and an empty memory file."""
    if agent_exists(agent_name):
        raise ValueError(f"Agent '{agent_name}' already exists.")

    config_path = get_agent_config_path(agent_name)
    memory_path = get_agent_memory_path(agent_name)

    agent_config = {
        "name": agent_name,
        "model": model,
        "created_at": json.dumps(str(os.path.getctime(config_path))) if os.path.exists(config_path) else None
    }

    with open(config_path, "w") as f:
        json.dump(agent_config, f, indent=4)

    # Create an empty memory file
    with open(memory_path, "w") as f:
        pass

    return agent_config

def delete_agent(agent_name: str):
    """Deletes an agent's config and memory files."""
    if not agent_exists(agent_name):
        raise ValueError(f"Agent '{agent_name}' not found.")

    os.remove(get_agent_config_path(agent_name))
    os.remove(get_agent_memory_path(agent_name))

def get_agent(agent_name: str) -> Dict[str, Any]:
    """Loads an agent's configuration."""
    if not agent_exists(agent_name):
        return None
    with open(get_agent_config_path(agent_name), "r") as f:
        return json.load(f)

def get_agent_memory(agent_name: str) -> List[Dict[str, str]]:
    """Loads an agent's conversation history from its memory file."""
    memory_path = get_agent_memory_path(agent_name)
    if not os.path.exists(memory_path):
        return []

    memory = []
    with open(memory_path, "r") as f:
        for line in f:
            memory.append(json.loads(line))
    return memory

def update_agent_memory(agent_name: str, user_prompt: str, assistant_response: str):
    """Appends a new user/assistant message pair to the agent's memory file."""
    memory_path = get_agent_memory_path(agent_name)

    new_entry = {
        "user": user_prompt,
        "assistant": assistant_response
    }

    with open(memory_path, "a") as f:
        f.write(json.dumps(new_entry) + "\n")

def edit_agent_memory(agent_name: str, new_memory: List[Dict[str, str]]):
    """Overwrites the agent's memory file with new content."""
    if not agent_exists(agent_name):
        raise ValueError(f"Agent '{agent_name}' not found.")

    memory_path = get_agent_memory_path(agent_name)
    with open(memory_path, "w") as f:
        for entry in new_memory:
            f.write(json.dumps(entry) + "\n")