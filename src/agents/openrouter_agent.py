"""OpenRouter Agent implementation."""

import os
import time
import json
import httpx
import openai
from typing import List, Dict, Optional

class OpenRouterAgent:
    """Agent that communicates with OpenRouter AI models."""
    
    def __init__(self, name: str, model: str, instruction: str):
        """Initialize the OpenRouter agent.
        
        Args:
            name: Name of the agent
            model: OpenRouter model ID (e.g., 'google/gemini-2.0-flash-001')
            instruction: System prompt/instruction for the agent
        """
        self.name = name
        self.model = model
        self.instruction = instruction
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
            
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/google-adk-multiagent", # Optional
                "X-Title": "Google ADK Multi-Agent System", # Optional
            },
            http_client=httpx.Client()
        )
        
    def query(self, text: str) -> str:
        """Send a query to the model via OpenRouter.
        
        Args:
            text: User input text
            
        Returns:
            Model response text
        """
        messages = [
            {"role": "system", "content": self.instruction},
            {"role": "user", "content": text}
        ]
        
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    # Optional: adjust parameters as needed
                    temperature=0.7,
                    max_tokens=4096,
                )
                
                if not response.choices:
                    return "Error: No response choices returned from OpenRouter."
                    
                return response.choices[0].message.content
                
            except openai.RateLimitError as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ OpenRouter Rate Limit hit (429). Waiting {retry_delay}s before retry {attempt + 1}/{max_retries}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    return f"Error: Rate limit exceeded after {max_retries} attempts. {str(e)}"
            except Exception as e:
                return f"Error contacting OpenRouter: {str(e)}"
        
        return "Error: Failed to get response after multiple attempts."

    def __repr__(self):
        return f"OpenRouterAgent(name='{self.name}', model='{self.model}')"
