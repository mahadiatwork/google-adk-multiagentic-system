"""CEO Agent implementation."""

from src.agents.base_agent import create_base_agent
from config.agent_configs import CEO_SYSTEM_PROMPT


def create_ceo_agent(model_name: str = None):
    """Create a CEO agent.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        Configured CEO agent
    """
    return create_base_agent(CEO_SYSTEM_PROMPT, model_name, agent_name="CEO")

