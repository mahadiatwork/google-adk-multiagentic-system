"""
Interactive script to run the Multi-Agent Development System.
Usage: python run_project.py
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

def run_project():
    print("=" * 60)
    print("🤖 Multi-Agent Development System (OpenRouter Enabled)")
    print("=" * 60)

    # Check API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Error: OPENROUTER_API_KEY not found!")
        print("Please set it in your .env file")
        sys.exit(1)

    # Get user input
    print("\nPlease provide project details:")
    print("-" * 30)
    
    default_name = "my_new_project"
    project_name = input(f"Project Name (default: {default_name}): ").strip() or default_name
    
    print("\nDescribe what you want to build (be descriptive!):")
    task_prompt = input("> ").strip()
    
    if not task_prompt:
        print("❌ Error: Task description cannot be empty.")
        sys.exit(1)

    output_dir = f"./output/{project_name}"
    
    print("\nConfiguration:")
    print(f"  Project: {project_name}")
    print(f"  Output:  {output_dir}")
    from config.agent_configs import DEFAULT_MODEL
    print(f"  Model:   {DEFAULT_MODEL} (via OpenRouter)")
    
    confirm = input("\nStart development? (y/n): ").lower()
    if confirm != 'y':
        print("Aborted.")
        sys.exit(0)
        
    print("\n🚀 Initializing Agents...")

    try:
        from src.state import DevelopmentState
        from src.chain.development_chain import create_development_chain
        
        # Initialize state
        state = DevelopmentState()
        state.task_prompt = task_prompt
        state.project_name = project_name
        state.output_directory = output_dir
        
        # Create chain with OpenRouter model
        from config.agent_configs import DEFAULT_MODEL
        chain = create_development_chain(
            model_name=DEFAULT_MODEL,
            max_review_iterations=3,
            max_test_iterations=3
        )
        
        # Run chain
        print("\n🔄 Starting development process...")
        result = chain.run(state.task_prompt, state=state)
        
        # Finish usage tracking
        if hasattr(state, 'usage_tracker'):
            state.usage_tracker.finish(model=DEFAULT_MODEL)
        
        print("\n" + "=" * 60)
        print("✅ Project Completed!")
        print("=" * 60)
        print(f"Output directory: {state.output_directory}")
        if hasattr(state, 'codes'):
            print(f"Files generated: {len(state.codes)}")
        print("\nCheck the output directory for your code.")
        
        # Print usage summary
        if hasattr(state, 'usage_tracker'):
            state.usage_tracker.print_summary()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you are in the project root.")
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_project()
