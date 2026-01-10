"""Programmer Agent implementation."""

from src.agents.base_agent import create_base_agent
from config.agent_configs import PROGRAMMER_SYSTEM_PROMPT


def create_programmer_agent(model_name: str = None):
    """Create a Programmer agent.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        Configured Programmer agent
    """
    return create_base_agent(PROGRAMMER_SYSTEM_PROMPT, model_name, agent_name="Programmer")

