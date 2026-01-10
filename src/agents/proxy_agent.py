"""Proxy Agent implementation for Antigravity Claude Proxy."""

import os
import httpx
import json
from httpx import Timeout

# ADK imports
try:
    from google.adk.agents import Agent
    from google.genai.types import Content, Part
except ImportError:
    # Use a dummy base if ADK is missing (for testing)
    class Agent:
        def __init__(self, name, model, instruction):
            self.name = name
            self.model = model
            self.instruction = instruction

class ProxyAgent(Agent):
    """Custom agent that routes requests to the Antigravity Claude Proxy."""
    
    def __init__(self, name: str, model: str, instruction: str, proxy_url: str = None, token: str = "test"):
        super().__init__(name=name, model=model, instruction=instruction)
        # Use object.__setattr__ to bypass Pydantic validation if Agent is a Pydantic model
        object.__setattr__(self, 'proxy_url', proxy_url or os.getenv("PROXY_URL", "http://localhost:8080"))
        object.__setattr__(self, 'token', token)
        object.__setattr__(self, 'client', httpx.Client(timeout=Timeout(120.0)))
        
    def query(self, text: str) -> str:
        """Sync query method (compatibility wrapper)."""
        # This is a synchronous blocking call
        messages = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": text}
        ]
        
        headers = {
            "x-api-key": self.token,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4096,
            "system": self.instruction # Anthropic usually passes system separately
        }
        
        # Adjust implementation for Anthropic API format
        # System instructions in top-level 'system' parameter, not in messages list
        payload["messages"] = [{"role": "user", "content": text}]
        
        try:
            response = self.client.post(
                f"{self.proxy_url}/v1/messages", 
                headers=headers, 
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract content from Anthropic format
            content_blocks = data.get("content", [])
            text_response = ""
            for block in content_blocks:
                if block.get("type") == "text":
                    text_response += block.get("text", "")
            
            return text_response
            
        except Exception as e:
            return f"Error contacting proxy: {str(e)}"

    def __call__(self, *args, **kwargs):
        """Allow calling agent like a function (similar to ADK agents in some contexts)."""
        # This is strictly not the ADK standard but helps with compatibility
        pass

    # Note: ADK Runners primarily use the internal handle methods, but for a custom
    # agent we might need to conform to how the Runner invokes it.
    # However, since we are hacking the ADK Runner in agent_runner.py anyway,
    # we might need to instantiate this Agent specially.
    # The ADK Runner expects a 'run' method that returns events/generator?
    # Actually, standard ADK Agents don't have a simple 'query'.
    # They are run explicitly by the Runner which handles the session.
    
    # We will implement a custom `.run` compatible with what we expect, 
    # but the REAL integration happens when we modify agent_runner.py or use a custom runner.
    # For now, let's assume we will swap the runner logic for this agent.
