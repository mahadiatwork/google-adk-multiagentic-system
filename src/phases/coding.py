"""Coding phase implementation."""

import re

from src.agents.cto_agent import create_cto_agent
from src.agents.programmer_agent import create_programmer_agent
from src.state import DevelopmentState
from src.tools.agent_runner import run_agent
from config.prompts import LANGUAGE_SELECTION_PROMPT, CODING_PROMPT
from src.tools.file_manager import create_project_directory


def extract_language(response: str) -> str:
    """Extract programming language from agent response.
    
    Args:
        response: Agent response text
        
    Returns:
        Extracted language string
    """
    # Look for <INFO>LANGUAGE</INFO> pattern
    pattern = r'<INFO>(.*?)</INFO>'
    matches = re.findall(pattern, response, re.IGNORECASE)
    
    if matches:
        return matches[0].strip()
    
    # Fallback: try to infer from response
    response_lower = response.lower()
    if 'python' in response_lower:
        return "Python"
    elif 'javascript' in response_lower or 'js' in response_lower:
        return "JavaScript"
    elif 'java' in response_lower:
        return "Java"
    elif 'c++' in response_lower or 'cpp' in response_lower:
        return "C++"
    else:
        return "Python"  # Default


def create_coding_phase(model_name: str = None):
    """Create the coding phase.
    
    Args:
        model_name: Optional model name override
        
    Returns:
        SequentialAgent for coding
    """
    cto_agent = create_cto_agent(model_name)
    programmer_agent = create_programmer_agent(model_name)
    
    def coding_handler(input_text: str, state: DevelopmentState):
        """Handler for coding phase."""
        # Step 1: Language selection
        lang_prompt = LANGUAGE_SELECTION_PROMPT.format(
            task_prompt=state.task_prompt,
            modality=state.modality
        )
        cto_response = run_agent(cto_agent, lang_prompt, state=state)
        # Track API usage
        state.usage_tracker.record_api_call_with_text(
            "CTO", "Coding", cto_agent.model,
            input_text=lang_prompt, output_text=str(cto_response)
        )
        language = extract_language(cto_response)
        state.language = language
        
        # Step 2: Code generation
        coding_prompt = CODING_PROMPT.format(
            task_prompt=state.task_prompt,
            modality=state.modality,
            language=language
        )
        programmer_response = run_agent(programmer_agent, coding_prompt, state=state)
        # Track API usage
        state.usage_tracker.record_api_call_with_text(
            "Programmer", "Coding", programmer_agent.model,
            input_text=coding_prompt, output_text=str(programmer_response)
        )
        
        # Extract and update codes
        state.update_codes(programmer_response)
        
        # Create output directory and save files
        if state.project_name:
            output_dir = create_project_directory(
                state.project_name,
                state.output_directory or "./output"
            )
            state.output_directory = output_dir
            state.save_to_directory()
        
        return f"Language selected: {language}\n\nCode generated:\n{programmer_response}"
    
    # Wrap with custom handler
    # We don't use SequentialAgent to avoid agent reuse issues
    class CodingPhase:
        def __init__(self, handler):
            self.handler = handler
        
        def run(self, input_text: str, state: DevelopmentState):
            return self.handler(input_text, state)
    
    return CodingPhase(coding_handler)

