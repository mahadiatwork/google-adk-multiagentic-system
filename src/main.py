"""Main entry point for the multi-agent development system."""

import argparse
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from src.state import DevelopmentState
from src.chain.development_chain import create_development_chain


def parse_arguments():
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Multi-agent software development system using Google ADK"
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Task description (what software to build)"
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Project name"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.0-flash-exp",
        help="Gemini model to use (default: gemini-2.0-flash-exp)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Output directory path (default: ./output)"
    )
    parser.add_argument(
        "--max-review-iterations",
        type=int,
        default=3,
        help="Maximum code review iterations (default: 3)"
    )
    parser.add_argument(
        "--max-test-iterations",
        type=int,
        default=3,
        help="Maximum test iterations (default: 3)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable not set")
        print("Please set it in your .env file or environment")
        sys.exit(1)
    
    # Parse arguments
    args = parse_arguments()
    
    # Initialize state
    state = DevelopmentState()
    state.task_prompt = args.task
    state.project_name = args.name
    state.output_directory = args.output_dir
    
    print("=" * 60)
    print("Google ADK Multi-Agent Development System")
    print("=" * 60)
    print(f"Task: {args.task}")
    print(f"Project: {args.name}")
    print(f"Model: {args.model}")
    print(f"Output: {args.output_dir}")
    print("=" * 60)
    print()
    
    # Create development chain
    chain = create_development_chain(
        model_name=args.model,
        max_review_iterations=args.max_review_iterations,
        max_test_iterations=args.max_test_iterations
    )
    
    # Execute chain
    try:
        import time
        start_time = time.time()
        result = chain.run(args.task, state=state)
        end_time = time.time()
        
        # Finish usage tracking
        state.usage_tracker.finish(model=args.model)
        
        print()
        print("=" * 60)
        print("Development Complete!")
        print("=" * 60)
        print(f"Output directory: {state.output_directory}")
        print(f"Files generated: {len(state.codes)}")
        for filename in state.codes.keys():
            print(f"  - {filename}")
        
        # Print usage summary
        state.usage_tracker.print_summary()
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

