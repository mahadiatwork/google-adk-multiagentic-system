
import os
from src.agents.base_agent import create_base_agent
import asyncio

# Mock environment for testing
os.environ["USE_PROXY"] = "true"
os.environ["ANTHROPIC_AUTH_TOKEN"] = "test"
os.environ["GOOGLE_API_KEY"] = "dummy" # Required by base_agent check

def test_proxy():
    print("Testing Proxy Integration...")
    
    # Create an agent that should default to ProxyAgent
    agent = create_base_agent(
        system_prompt="You are a helpful assistant.",
        agent_name="ProxyTester",
        model_name="gemini-3-flash"
    )
    
    print(f"Agent Type: {type(agent).__name__}")
    
    if type(agent).__name__ != "ProxyAgent":
        print("❌ Failed: Agent is not a ProxyAgent")
        return

    # Check query capability
    print("Attempting to query proxy (requires executing 'antigravity-claude-proxy start' externally)...")
    
    try:
        # We need to access the client directly for better debugging since query() swallows errors
        import httpx
        system = "You are a helpful assistant."
        text = "Hello, assume you are a robot."
        
        headers = {
            "x-api-key": agent.token,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": agent.model,
            "messages": [{"role": "user", "content": text}],
            "max_tokens": 1024,
            "system": system
        }
        
        print(f"Sending request to {agent.proxy_url}/v1/messages...")
        response = agent.client.post(
            f"{agent.proxy_url}/v1/messages", 
            headers=headers, 
            json=payload
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error Response: {response.text}")
        else:
            data = response.json()
            print(f"Success Response keys: {data.keys()}")
            print(f"Full Response: {data}")

    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_proxy()
