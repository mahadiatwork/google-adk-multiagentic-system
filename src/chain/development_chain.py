"""Main development chain orchestrator."""

try:
    from google.adk.agents import SequentialAgent
except ImportError:
    SequentialAgent = None

from src.state import DevelopmentState
from src.phases.demand_analysis import create_demand_analysis_phase
from src.phases.coding import create_coding_phase
from src.phases.code_review import create_code_review_phase
from src.phases.testing import create_testing_phase


def create_development_chain(model_name: str = None, max_review_iterations: int = 3, max_test_iterations: int = 3):
    """Create the main development chain.
    
    Args:
        model_name: Optional model name override
        max_review_iterations: Maximum review loop iterations
        max_test_iterations: Maximum test loop iterations
        
    Returns:
        SequentialAgent representing the full development chain
    """
    # Create all phases
    demand_analysis = create_demand_analysis_phase(model_name)
    coding = create_coding_phase(model_name)
    code_review = create_code_review_phase(model_name, max_review_iterations)
    testing = create_testing_phase(model_name, max_test_iterations)
    
    # Create a wrapper that handles state properly
    class DevelopmentChain:
        def __init__(self, phases):
            self.phases = phases
        
        def run(self, input_text: str, state: DevelopmentState = None):
            """Run the development chain.
            
            Args:
                input_text: Initial task description
                state: Development state (will be created if not provided)
                
            Returns:
                Final result from the chain
            """
            if state is None:
                state = DevelopmentState()
                state.task_prompt = input_text
            
            # Run each phase sequentially
            current_input = input_text
            results = []
            
            try:
                # Phase 1: Demand Analysis
                print("Phase 1: Demand Analysis...")
                result1 = demand_analysis.run(current_input, state)
                results.append(("Demand Analysis", result1))
                print(f"Modality: {state.modality}")
                
                # Phase 2: Coding
                print("Phase 2: Coding...")
                result2 = coding.run(current_input, state)
                results.append(("Coding", result2))
                print(f"Language: {state.language}")
                print(f"Files generated: {list(state.codes.keys())}")
                
                # Phase 3: Code Review
                print("Phase 3: Code Review...")
                result3 = code_review.run(current_input, state)
                results.append(("Code Review", result3))
                
                # Phase 4: Testing
                print("Phase 4: Testing...")
                result4 = testing.run(current_input, state)
                results.append(("Testing", result4))
                
                # Final summary
                summary = "\n\n".join([f"{phase}:\n{result}" for phase, result in results])
                return summary
                
            except Exception as e:
                error_msg = f"Error in development chain: {str(e)}"
                print(error_msg)
                return f"{error_msg}\n\nPartial results:\n" + "\n\n".join([f"{phase}:\n{result}" for phase, result in results])
    
    return DevelopmentChain([demand_analysis, coding, code_review, testing])

