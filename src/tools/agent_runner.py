"""Utility to run agents properly."""

import os
import asyncio

def run_agent(agent, input_text: str, state=None):
    """Run an agent with the given input.
    
    Args:
        agent: Agent instance to run (expected to be OpenRouterAgent)
        input_text: Input text for the agent
        state: Optional state object
        
    Returns:
        Agent response as string
    """
    # Check if agent has query method (OpenRouterAgent)
    if hasattr(agent, 'query'):
        try:
            return agent.query(input_text)
        except Exception as e:
            return f"Error running agent {getattr(agent, 'name', 'unknown')}: {str(e)}"
    
    return "Error: Unsupported agent type. This system now requires OpenRouterAgent."
