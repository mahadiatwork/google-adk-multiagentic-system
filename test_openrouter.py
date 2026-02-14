"""Verification script for OpenRouter integration."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

def test_openrouter():
    print("=" * 60)
    print("OpenRouter Integration Test")
    print("=" * 60)
    
    # 1. Check API Key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in .env")
        return
    print("[OK] OPENROUTER_API_KEY found")
    
    # 2. Check Model
    from config.agent_configs import DEFAULT_MODEL
    model = os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
    print(f"DEBUG: Testing model: {model}")
    
    # 3. Initialize Agent
    print("\nInitializing OpenRouterAgent...")
    try:
        from src.agents.base_agent import create_base_agent
        agent = create_base_agent(
            system_prompt="You are a helpful assistant.",
            agent_name="TestAgent",
            model_name=model
        )
        print(f"[OK] Agent initialized: {type(agent).__name__}")
    except Exception as e:
        import traceback
        print(f"[ERR] Initialization failed: {e}")
        traceback.print_exc()
        return
    
    # 4. Perform Test Query
    print("\nSending test query to OpenRouter...")
    print("(This verifies connectivity and API key validity)")
    
    try:
        from src.tools.agent_runner import run_agent
        response = run_agent(agent, "Say 'Hello, OpenRouter is working!'")
        
        print(f"\nResponse: {response}")
        
        if "working" in response.lower():
            print("\n[SUCCESS] OpenRouter integration is fully functional!")
        else:
            print("\n⚠️ Received response but it might not be what was expected.")
            
    except Exception as e:
        print(f"\n❌ Execution failed: {e}")

if __name__ == "__main__":
    test_openrouter()
