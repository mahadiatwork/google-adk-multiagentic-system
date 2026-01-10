"""CTO Agent implementation."""

from src.agents.base_agent import create_base_agent
from config.agent_configs import CTO_SYSTEM_PROMPT


def create_cto_agent(model_name: str = None):
    """Create a CTO agent.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        Configured CTO agent
    """
    return create_base_agent(CTO_SYSTEM_PROMPT, model_name, agent_name="CTO")

