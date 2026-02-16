import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.test_runner import execute_and_heal

def test_self_healing():
    # 1. Create a bad code file
    bad_code_path = "bad_code.py"
    with open(bad_code_path, "w") as f:
        f.write("print('Starting bad code...')\n")
        f.write("print(1 / 0) # This will crash\n")
    
    print(f"--- Testing Self-Healing with {bad_code_path} ---")
    
    # 2. Run the healer
    success = execute_and_heal(bad_code_path, max_retries=3)
    
    # 3. Verify the outcome
    print(f"\nFinal Success Status: {success}")
    
    # 4. Cleanup (optional, but good for inspection first)
    # os.remove(bad_code_path)

if __name__ == "__main__":
    test_self_healing()
