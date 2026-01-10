"""Code Reviewer Agent implementation."""

from src.agents.base_agent import create_base_agent
from config.agent_configs import REVIEWER_SYSTEM_PROMPT


def create_reviewer_agent(model_name: str = None):
    """Create a Code Reviewer agent.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        Configured Reviewer agent
    """
    return create_base_agent(REVIEWER_SYSTEM_PROMPT, model_name, agent_name="Reviewer")

