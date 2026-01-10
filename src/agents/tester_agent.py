"""Test Engineer Agent implementation."""

from src.agents.base_agent import create_base_agent
from config.agent_configs import TESTER_SYSTEM_PROMPT


def create_tester_agent(model_name: str = None):
    """Create a Test Engineer agent.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        Configured Tester agent
    """
    return create_base_agent(TESTER_SYSTEM_PROMPT, model_name, agent_name="Tester")

