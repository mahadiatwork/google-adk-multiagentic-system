"""Demand Analysis phase implementation."""

import re

from src.agents.ceo_agent import create_ceo_agent
from src.agents.cpo_agent import create_cpo_agent
from src.state import DevelopmentState
from src.tools.agent_runner import run_agent
from config.prompts import DEMAND_ANALYSIS_PROMPT


def extract_modality(response: str) -> str:
    """Extract modality from agent response.
    
    Args:
        response: Agent response text
        
    Returns:
        Extracted modality string
    """
    # Look for <INFO>MODALITY</INFO> pattern
    pattern = r'<INFO>(.*?)</INFO>'
    matches = re.findall(pattern, response, re.IGNORECASE)
    
    if matches:
        return matches[0].strip()
    
    # Fallback: try to infer from response
    response_lower = response.lower()
    if 'website' in response_lower or 'web' in response_lower:
        return "Website"
    elif 'application' in response_lower or 'app' in response_lower:
        return "Application"
    elif 'game' in response_lower:
        return "Game"
    elif 'cli' in response_lower or 'command' in response_lower:
        return "CLI Tool"
    else:
        return "Application"  # Default


def create_demand_analysis_phase(model_name: str = None):
    """Create the demand analysis phase.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        SequentialAgent for demand analysis
    """
    ceo_agent = create_ceo_agent(model_name)
    cpo_agent = create_cpo_agent(model_name)
    
    def demand_analysis_handler(input_text: str, state: DevelopmentState):
        """Handler for demand analysis phase."""
        prompt = DEMAND_ANALYSIS_PROMPT.format(task_prompt=state.task_prompt)
        
        # Run CEO agent
        ceo_response = run_agent(ceo_agent, prompt, state=state)
        # Track API usage
        state.usage_tracker.record_api_call_with_text(
            "CEO", "Demand Analysis", ceo_agent.model,
            input_text=prompt, output_text=str(ceo_response)
        )
        
        # Run CPO agent with CEO's analysis
        cpo_prompt = f"{prompt}\n\nCEO Analysis:\n{ceo_response}"
        cpo_response = run_agent(cpo_agent, cpo_prompt, state=state)
        # Track API usage
        state.usage_tracker.record_api_call_with_text(
            "CPO", "Demand Analysis", cpo_agent.model,
            input_text=cpo_prompt, output_text=str(cpo_response)
        )
        
        # Extract modality
        modality = extract_modality(cpo_response)
        state.modality = modality
        
        return f"Modality determined: {modality}\n\nCPO Response: {cpo_response}"
    
    # Wrap with custom handler to extract modality
    # We don't use SequentialAgent to avoid agent reuse issues
    class DemandAnalysisPhase:
        def __init__(self, handler):
            self.handler = handler
        
        def run(self, input_text: str, state: DevelopmentState):
            return self.handler(input_text, state)
    
    return DemandAnalysisPhase(demand_analysis_handler)

