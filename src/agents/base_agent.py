"""Base agent utilities and factory functions."""

import os

try:
    from google.adk.agents import LlmAgent
    from google import generativeai as genai
except ImportError:
    # Fallback for development/testing without ADK installed
    LlmAgent = None
    genai = None

from config.agent_configs import DEFAULT_MODEL, DEFAULT_TEMPERATURE


def get_model(model_name: str = None) -> str:
    """Get the model name to use.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        Model name string
    """
    return model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)


def create_base_agent(system_prompt: str, model_name: str = None, agent_name: str = "agent"):
    """Create a base LLM agent with the given system prompt.
    
    Args:
        system_prompt: System prompt for the agent
        model_name: Optional model name override
        agent_name: Name for the agent (default: "agent")
        
    Returns:
        Configured LlmAgent instance
    """
    if LlmAgent is None:
        raise ImportError("google-adk is not installed. Please install it with: pip install google-adk")
    
    # Configure API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    # Check for proxy usage
    from config.agent_configs import USE_PROXY, PROXY_URL, MODEL_CLAUDE_SONNET
    
    # Use proxy if configured or if model name is a proxy-specific model
    should_use_proxy = USE_PROXY or (model_name and ("claude" in model_name or "gemini-3" in model_name))
    
    if should_use_proxy:
        from src.agents.proxy_agent import ProxyAgent
        token = os.getenv("ANTHROPIC_AUTH_TOKEN", "test")
        
        # Determine actual model name if needed
        # If model_name is None, use default proxy model
        final_model = model_name or MODEL_CLAUDE_SONNET
        
        agent = ProxyAgent(
            name=agent_name,
            model=final_model,
            instruction=system_prompt,
            proxy_url=PROXY_URL,
            token=token
        )
        return agent

    if genai:
        genai.configure(api_key=api_key)
    
    model = get_model(model_name)
    
    # Create agent with correct parameters
    # Note: temperature is not directly supported, it may be in model config
    agent = LlmAgent(
        name=agent_name,
        model=model,
        instruction=system_prompt
    )
    
    return agent

