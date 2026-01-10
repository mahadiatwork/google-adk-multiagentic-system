"""Testing phase implementation."""

from src.agents.tester_agent import create_tester_agent
from src.agents.programmer_agent import create_programmer_agent
from src.state import DevelopmentState
from src.tools.agent_runner import run_agent
from config.prompts import TESTING_PROMPT, FIX_CODE_PROMPT
from src.tools.test_runner import run_tests, parse_test_errors


def test_condition(result: str, state: DevelopmentState) -> bool:
    """Determine if testing loop should continue.
    
    Args:
        result: Last agent response
        state: Development state
        
    Returns:
        True if loop should continue (errors found), False otherwise
    """
    # Check if tester found errors
    if "<INFO>No errors</INFO>" in result or "<INFO> No errors</INFO>" in result:
        return False
    
    # Check state for error summary
    if state.error_summary and "error" in state.error_summary.lower():
        return True
    
    # Check if result indicates errors
    result_lower = result.lower()
    error_keywords = ["error", "fail", "bug", "issue", "problem"]
    return any(keyword in result_lower for keyword in error_keywords)


def create_testing_phase(model_name: str = None, max_iterations: int = 3):
    """Create the testing phase with loop.
    
    Args:
        model_name: Optional model name override
        max_iterations: Maximum number of test iterations
        
    Returns:
        TestingPhase instance
    """
    tester_agent = create_tester_agent(model_name)
    programmer_agent = create_programmer_agent(model_name)
    
    def test_handler(input_text: str, state: DevelopmentState):
        """Handler for test iteration."""
        # Run tests
        if state.output_directory and state.language:
            success, test_output = run_tests(state.output_directory, state.language)
            state.test_reports = test_output
            
            # Parse errors
            if not success:
                state.error_summary = parse_test_errors(test_output)
            else:
                state.error_summary = ""
        else:
            test_output = "Tests not run (missing directory or language)"
            state.test_reports = test_output
            state.error_summary = ""
        
        # Tester analyzes results
        test_prompt = TESTING_PROMPT.format(
            task_prompt=state.task_prompt,
            language=state.language,
            test_reports=state.test_reports,
            error_summary=state.error_summary,
            codes=state.get_codes_formatted()
        )
        from config.agent_configs import DEFAULT_MODEL
        default_model = model_name or DEFAULT_MODEL
        tester_response = run_agent(tester_agent, test_prompt, state=state)
        # Track API usage
        state.usage_tracker.record_api_call_with_text(
            "Tester", "Testing", default_model,
            input_text=test_prompt, output_text=str(tester_response)
        )
        
        # Check if no errors
        if "<INFO>No errors</INFO>" in tester_response or "<INFO> No errors</INFO>" in tester_response:
            return tester_response
        
        # Programmer fixes code
        fix_prompt = FIX_CODE_PROMPT.format(
            task_prompt=state.task_prompt,
            language=state.language,
            feedback=tester_response,
            codes=state.get_codes_formatted()
        )
        fix_response = run_agent(programmer_agent, fix_prompt, state=state)
        # Track API usage
        state.usage_tracker.record_api_call_with_text(
            "Programmer", "Testing", default_model,
            input_text=fix_prompt, output_text=str(fix_response)
        )
        
        # Update codes
        state.update_codes(fix_response)
        state.save_to_directory()
        
        return f"Test Analysis: {tester_response}\n\nFixes applied: {fix_response}"
    
    # Wrap with custom handler that implements the loop logic
    # We use a custom handler instead of LoopAgent to have full control over the condition
    # and avoid agent reuse issues
    class TestingPhase:
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
            return result or "Testing completed"
    
    return TestingPhase(test_handler, test_condition, max_iterations)

