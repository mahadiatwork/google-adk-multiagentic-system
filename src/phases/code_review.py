"""Code Review phase implementation."""

from src.agents.reviewer_agent import create_reviewer_agent
from src.agents.programmer_agent import create_programmer_agent
from src.state import DevelopmentState
from src.tools.agent_runner import run_agent
from config.prompts import CODE_REVIEW_PROMPT, FIX_CODE_PROMPT


def review_condition(result: str, state: DevelopmentState) -> bool:
    """Determine if review loop should continue.
    
    Args:
        result: Last agent response
        state: Development state
        
    Returns:
        True if loop should continue, False otherwise
    """
    return "<INFO>Finished</INFO>" not in result and "<INFO> Finished</INFO>" not in result


def create_code_review_phase(model_name: str = None, max_iterations: int = 3):
    """Create the code review phase with loop.
    
    Args:
        model_name: Optional model name override
        max_iterations: Maximum number of review iterations
        
    Returns:
        CodeReviewPhase instance
    """
    reviewer_agent = create_reviewer_agent(model_name)
    programmer_agent = create_programmer_agent(model_name)
    
    def review_handler(input_text: str, state: DevelopmentState):
        """Handler for review iteration."""
        # Reviewer analyzes code
        review_prompt = CODE_REVIEW_PROMPT.format(
            task_prompt=state.task_prompt,
            language=state.language,
            codes=state.get_codes_formatted()
        )
        from config.agent_configs import DEFAULT_MODEL
        default_model = model_name or DEFAULT_MODEL
        review_response = run_agent(reviewer_agent, review_prompt, state=state)
        # Track API usage
        state.usage_tracker.record_api_call_with_text(
            "Reviewer", "Code Review", default_model,
            input_text=review_prompt, output_text=str(review_response)
        )
        
        # Check if finished
        if "<INFO>Finished</INFO>" in review_response or "<INFO> Finished</INFO>" in review_response:
            state.review_comments = "Code review passed"
            return review_response
        
        # Update review comments
        state.review_comments = review_response
        
        # Programmer fixes code
        fix_prompt = FIX_CODE_PROMPT.format(
            task_prompt=state.task_prompt,
            language=state.language,
            feedback=review_response,
            codes=state.get_codes_formatted()
        )
        fix_response = run_agent(programmer_agent, fix_prompt, state=state)
        # Track API usage
        state.usage_tracker.record_api_call_with_text(
            "Programmer", "Code Review", default_model,
            input_text=fix_prompt, output_text=str(fix_response)
        )
        
        # Update codes
        state.update_codes(fix_response)
        state.save_to_directory()
        
        return f"Review: {review_response}\n\nFixes applied: {fix_response}"
    
    # Wrap with custom handler that implements the loop logic
    # We use a custom handler instead of LoopAgent to have full control over the condition
    # and avoid agent reuse issues
    class CodeReviewPhase:
        def __init__(self, handler, condition_func, max_iterations):
            self.handler = handler
            self.condition_func = condition_func
            self.max_iterations = max_iterations
        
        def run(self, input_text: str, state: DevelopmentState):
            # Manual loop with condition check
            result = None
            for i in range(self.max_iterations):
                result = self.handler(input_text, state)
                if not self.condition_func(result, state):
                    break
            return result or "Code review completed"
    
    return CodeReviewPhase(review_handler, review_condition, max_iterations)

