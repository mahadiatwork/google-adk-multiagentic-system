# Testing Guide

## Quick Start Testing

### Step 1: Verify Basic Functionality (✅ Already Passed)
The unit tests verify core functionality:
```bash
python -m unittest tests.test_basic_flow -v
```

### Step 2: Test with a Simple Task

Run the simple test script:
```bash
python test_simple.py
```

This will:
- Verify your API key is set
- Test imports
- Run a simple "hello world" task
- Generate code in `./test_output/test_hello/`

### Step 3: Test with Main Entry Point

Run the full system with a simple task:
```bash
python src/main.py --task "Create a Python hello world program" --name "hello_world"
```

Or with more options:
```bash
python src/main.py \
  --task "Create a simple calculator with add, subtract, multiply, and divide functions" \
  --name "calculator" \
  --model "gemini-pro" \
  --max-review-iterations 2 \
  --max-test-iterations 2
```

## Test Examples

### Example 1: Simple Python Program
```bash
python src/main.py --task "Create a Python program that prints 'Hello, World!'" --name "hello"
```

### Example 2: Calculator
```bash
python src/main.py --task "Create a simple calculator class in Python with add, subtract, multiply, and divide methods" --name "calculator"
```

### Example 3: Web Application
```bash
python src/main.py --task "Create a simple HTML page with a button that shows an alert when clicked" --name "web_app"
```

### Example 4: Data Processing
```bash
python src/main.py --task "Create a Python script that reads a CSV file and prints the first 5 rows" --name "csv_reader"
```

## What to Expect

The system will go through 4 phases:

1. **Phase 1: Demand Analysis** (CEO + CPO)
   - Determines product modality (Application, Website, etc.)
   - Output: Modality type

2. **Phase 2: Coding** (CTO + Programmer)
   - Selects programming language
   - Generates code files
   - Output: Language and generated files

3. **Phase 3: Code Review** (Reviewer + Programmer loop)
   - Reviews code quality
   - Fixes issues iteratively
   - Output: Review feedback and fixes

4. **Phase 4: Testing** (Tester + Programmer loop)
   - Runs tests
   - Fixes bugs
   - Output: Test results and fixes

## Output Location

Generated code will be saved in:
- Default: `./output/{project_name}/`
- Or custom: Use `--output-dir` argument

## Troubleshooting

### API Key Issues
If you see "GOOGLE_API_KEY environment variable not set":
1. Create a `.env` file in the project root
2. Add: `GOOGLE_API_KEY=your_key_here`
3. Or set it as an environment variable

### Import Errors
If you see import errors:
```bash
pip install -r requirements.txt
```

### Model Not Found
If you see model errors, try:
- `--model gemini-1.5-pro`
- `--model gemini-1.5-flash`
- Check available models in Google AI Studio

### Code Not Extracted
If code isn't being extracted:
- Check the output directory for any generated files
- Review the console output for agent responses
- The code extraction may need adjustment based on actual LLM response format

## Advanced Testing

### Test Individual Components

Test state management:
```python
from src.state import DevelopmentState
state = DevelopmentState()
state.task_prompt = "Test task"
print(state.task_prompt)
```

Test code extraction:
```python
from src.tools.code_manager import extract_code_blocks
text = "main.py\n```python\nprint('Hello')\n```"
codes = extract_code_blocks(text)
print(codes)
```

### Verbose Output
The system prints progress at each phase. Watch for:
- Phase completion messages
- Modality and language selection
- File generation
- Review and test iterations

## Success Indicators

✅ **Successful run shows:**
- All 4 phases complete
- Modality determined
- Language selected
- Files generated (list shown)
- Output directory path

❌ **If errors occur:**
- Check API key is valid
- Verify model name is correct
- Check internet connection
- Review error traceback for details





