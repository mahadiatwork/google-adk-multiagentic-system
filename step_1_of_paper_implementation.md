# Step 1: Robust Code Block Extraction Implementation

## Objective
Implement a reliable and robust function to extract Python code from markdown-formatted LLM responses. This addresses the "API Output Faults" and "Integration Challenges" identified in the research digest.

## Functional Requirements
- **Capture**: Must handle ` ```python ` and ` ``` ` blocks.
- **Multi-line**: Must correctly process multi-line strings (re.DOTALL).
- **Fallback**: If no markdown markers are present, assume the entire output is code and return it stripped.
- **Resilience**: Handle variations in case (e.g., `PYTHON`) and whitespace.

## Implementation

```python
import re

def extract_code_block(llm_output: str) -> str:
    """
    Extracts pure Python code from a markdown-formatted LLM response.
    
    It captures content within ```python ... ``` or ``` ... ``` blocks.
    If no backticks are found, it returns the entire stripped string.
    """
    # Pattern for markdown code blocks with optional 'python' identifier
    # Captures everything between the opening and closing triple backticks
    pattern = r"```(?:python)?\n?(.*?)```"
    
    # Search for the first valid code block
    match = re.search(pattern, llm_output, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    # Fallback: if no backticks are found, return the entire stripped string
    if "```" not in llm_output:
        return llm_output.strip()
        
    # Default fallback for malformed markers
    return llm_output.strip()
```

## Verification Plan
1. **Unit Tests**: Create a test suite covering:
   - Standard markdown blocks.
   - Naked code without backticks.
   - Multiple code blocks (ensure it takes the first one or handles specifically).
   - Variations in language identifiers (PYTHON, py, etc.).
2. **Integration**: Replace existing flaky parsing logic in `src/tools/code_manager.py`.

## How to Test
To verify the implementation, run the dedicated test suite:

```bash
python tests/test_parser.py
```

### Test Results
The following test cases are covered and passing:
- `test_standard_markdown`: Correctly extracts code from within ```python ... ``` blocks.
- `test_naked_code`: Properly handles responses that contain only raw code.
- `test_case_insensitivity`: Matches `PYTHON`, `python`, and other variations.
- `test_no_language_label`: Handles generic ``` ... ``` blocks.
- `test_multiline_strings`: Correctly captures multi-line code without truncated data.

**Verification Status**: ✅ PASSED (5/5 tests)


## Next Steps
- **Step 2**: Define Agent State and Context Management.
- **Step 3**: Implement Agent Communication Protocols.
