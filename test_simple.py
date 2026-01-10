"""Simple test script to verify the system works."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Check API key
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Error: GOOGLE_API_KEY not found!")
    print("Please set it in your .env file or environment variables")
    sys.exit(1)

print("✅ API Key found")
print()

# Test basic imports
print("Testing imports...")
try:
    from src.state import DevelopmentState
    from src.chain.development_chain import create_development_chain
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

print()

# Test with a simple task
print("=" * 60)
print("Running Simple Test")
print("=" * 60)
print("Task: Create a simple Python hello world program")
print()

try:
    from src.state import DevelopmentState
    from src.chain.development_chain import create_development_chain
    
    # Initialize state
    state = DevelopmentState()
    state.task_prompt = "Create a simple Python hello world program"
    state.project_name = "test_hello"
    state.output_directory = "./test_output"
    
    # Create development chain
    # Using gemini-3-flash to verify proxy integration
    print("Creating development chain...")
    chain = create_development_chain(
        model_name="gemini-3-flash",
        max_review_iterations=1,  # Reduced for quick test
        max_test_iterations=1     # Reduced for quick test
    )
    print("✅ Chain created")
    print()
    
    # Run chain
    print("Starting development process...")
    print("(This may take a few minutes)")
    print()
    
    result = chain.run(state.task_prompt, state=state)
    
    # Finish usage tracking
    state.usage_tracker.finish(model="gemini-2.0-flash-exp")
    
    print()
    print("=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
    print(f"Output directory: {state.output_directory}")
    print(f"Files generated: {len(state.codes)}")
    for filename in state.codes.keys():
        print(f"  - {filename}")
    print()
    print("Check the output directory for generated files!")
    
    # Print usage summary
    state.usage_tracker.print_summary()
    
except Exception as e:
    print(f"❌ Error during execution: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

