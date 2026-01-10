"""CPO Agent implementation."""

from src.agents.base_agent import create_base_agent
from config.agent_configs import CPO_SYSTEM_PROMPT


def create_cpo_agent(model_name: str = None):
    """Create a CPO agent.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        Configured CPO agent
    """
    return create_base_agent(CPO_SYSTEM_PROMPT, model_name, agent_name="CPO")

