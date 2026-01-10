# Troubleshooting Guide

## Common Issues and Solutions

### ModuleNotFoundError: No module named 'src'

**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
This has been fixed in the code. The `src/main.py` file now automatically adds the project root to the Python path. 

If you still encounter this error:
1. Make sure you're running from the project root directory
2. Ensure you're using the latest version of the code
3. Try running: `python -m src.main --task "your task" --name "project_name"`

### GOOGLE_API_KEY not found

**Error:**
```
Error: GOOGLE_API_KEY environment variable not set
```

**Solution:**
1. Create a `.env` file in the project root
2. Add your API key: `GOOGLE_API_KEY=your_key_here`
3. Or set it as an environment variable:
   - Windows: `set GOOGLE_API_KEY=your_key_here`
   - Linux/Mac: `export GOOGLE_API_KEY=your_key_here`

### Import Errors

**Error:**
```
ImportError: google-adk is not installed
```

**Solution:**
```bash
pip install -r requirements.txt
```

### Model Not Found

**Error:**
```
Model not found or API error
```

**Solution:**
1. Check that your API key is valid
2. Try a different model: `--model gemini-1.5-pro` or `--model gemini-1.5-flash`
3. Verify your Google Cloud/Gemini API access

### Code Not Being Extracted

**Issue:**
Code files are not being generated or saved.

**Solution:**
1. Check the console output for agent responses
2. Verify the output directory exists and is writable
3. Review the code extraction patterns in `src/tools/code_manager.py`
4. The LLM response format may need adjustment

### Permission Errors

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
1. Check file/directory permissions
2. Ensure the output directory is writable
3. On Windows, you may need to run as administrator

### Test Execution Errors

**Error:**
```
Test execution fails or hangs
```

**Solution:**
1. Ensure the programming language runtime is installed (Python, Node.js, etc.)
2. Check that test files are properly formatted
3. Review test output in the console
4. Try reducing `--max-test-iterations` for debugging

## Getting Help

If you encounter other issues:

1. Check the console output for detailed error messages
2. Review the traceback for specific line numbers
3. Verify all dependencies are installed: `pip list`
4. Ensure you're using Python 3.8 or higher
5. Check that you're in the correct directory

## Verification Steps

To verify your setup is correct:

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Verify dependencies:**
   ```bash
   pip list | grep google-adk
   pip list | grep python-dotenv
   ```

3. **Test imports:**
   ```bash
   python -c "from src.state import DevelopmentState; print('OK')"
   ```

4. **Run unit tests:**
   ```bash
   python -m unittest tests.test_basic_flow -v
   ```

5. **Run simple test:**
   ```bash
   python test_simple.py
   ```





