"""Base agent utilities and factory functions."""

import os
from config.agent_configs import DEFAULT_MODEL, DEFAULT_TEMPERATURE
from src.agents.openrouter_agent import OpenRouterAgent


def get_model(model_name: str = None, role: str = None) -> str:
    """Get the model name to use.
    
    Args:
        model_name: Optional model name override
        role: Optional role name (e.g., 'CEO', 'PROGRAMMER')
        
    Returns:
        Model name string
    """
    if model_name:
        return model_name
        
    if role:
        # Check for role-specific environment variable (e.g., MODEL_CEO)
        env_role_model = os.getenv(f"MODEL_{role.upper()}")
        if env_role_model:
            return env_role_model
            
    # Fallback order: OPENROUTER_MODEL -> DEFAULT_MODEL
    return os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")


def create_base_agent(system_prompt: str, model_name: str = None, agent_name: str = "agent"):
    """Create an OpenRouter-based agent with the given system prompt.
    
    Args:
        system_prompt: System prompt for the agent
        model_name: Optional model name override
        agent_name: Name for the agent (default: "agent")
        
    Returns:
        Configured OpenRouterAgent instance
    """
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    
    model = get_model(model_name, role=agent_name)
    
    # Create OpenRouter agent
    agent = OpenRouterAgent(
        name=agent_name,
        model=model,
        instruction=system_prompt
    )
    
    return agent
