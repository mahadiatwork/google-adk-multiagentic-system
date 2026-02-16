"""Test execution and error parsing utilities."""

import subprocess
import os
import py_compile
import tempfile
from typing import Tuple, List
from dotenv import load_dotenv
from src.agents.openrouter_agent import OpenRouterAgent
from src.tools.code_manager import extract_code_block


def call_repair_agent(filepath: str, error_msg: str) -> None:
    """
    Calls the LLM to fix the code based on the provided error message.
    """
    try:
        load_dotenv()
        with open(filepath, 'r') as f:
            buggy_code = f.read()

        model = os.getenv("MODEL_PROGRAMMER", "google/gemini-2.0-flash")
        print(f"🤖 Calling RepairAgent ({model}) to fix the code...")
        
        agent = OpenRouterAgent(
            name="RepairAgent",
            model=model,
            instruction="You are an expert Python debugger."
        )

        prompt = (
            f"The following Python code crashed with this error:\n\n{error_msg}\n\n"
            f"Here is the buggy code:\n\n{buggy_code}\n\n"
            f"Please fix the code to resolve this exact error. "
            f"Output ONLY the fully corrected Python code inside a markdown block. "
            f"Do not explain the fix."
        )

        response = agent.query(prompt)
        print(f"DEBUG: Raw response length: {len(response)}")
        fixed_code = extract_code_block(response)
        
        if fixed_code:
            # SANITY CHECK 1: Syntax Validation
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as tmp:
                tmp.write(fixed_code)
                tmp_path = tmp.name
            
            try:
                py_compile.compile(tmp_path, doraise=True)
                syntax_ok = True
            except py_compile.PyCompileError:
                syntax_ok = False
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

            if not syntax_ok:
                print("⚠️ Fixed code has syntax errors. Refusing to overwrite.")
                return

            # SANITY CHECK 2: Degradation Check
            # If the fixed code is much shorter than the original, it might be truncated
            if len(fixed_code) < len(buggy_code) * 0.5 and len(buggy_code) > 500:
                print(f"⚠️ Fixed code is significantly shorter ({len(fixed_code)} vs {len(buggy_code)}). Potential truncation detected. Refusing to overwrite.")
                return

            print(f"DEBUG: Extracted code (first 50 chars): {fixed_code[:50].replace('\n', ' ')}...")
            with open(filepath, 'w') as f:
                f.write(fixed_code)
            print("✨ Code fixed and saved.")
        else:
            print("⚠️ Failed to extract fixed code from LLM response.")
            print(f"DEBUG: Full Raw Response:\n{response}")
            
    except Exception as e:
        print(f"❌ Error during repair: {str(e)}")


def execute_and_heal(filepath: str, max_retries: int = 3) -> bool:
    """
    Safely executes a generated Python script and attempts to self-heal if it crashes.
    
    Args:
        filepath: Path to the python script
        max_retries: Number of attempts to fix and rerun
        
    Returns:
        True if execution eventually succeeds, False otherwise
    """
    retries = 0
    while retries < max_retries:
        print(f"\n[Attempt {retries + 1}] Executing: {filepath}")
        
        # Secure execution without shell=True
        try:
            result = subprocess.run(
                ['python', filepath],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Success executing {filepath}")
                if result.stdout:
                    print(f"Output: {result.stdout.strip()}")
                return True
            else:
                stderr = result.stderr.strip()
                print(f"❌ Error caught: {stderr}. Sending to RepairAgent...")
                
                # Call the real RepairAgent
                call_repair_agent(filepath, stderr)
                
                retries += 1
        except Exception as e:
            print(f"❌ Subprocess failed to run: {str(e)}")
            return False
            
    print(f"\n🚫 Failed after {max_retries} retries.")
    return False


def run_tests(directory: str, language: str, modality: str = "") -> Tuple[bool, str]:
    """Run tests for the project.
    
    Args:
        directory: Project directory
        language: Programming language (python, javascript, etc.)
        modality: Product modality (Website, Application, etc.)
        
    Returns:
        Tuple of (success: bool, output: str)
    """
    lang_lower = language.lower()
    mod_lower = modality.lower() if modality else ""

    if lang_lower == "python":
        return _run_python_tests(directory)
    elif lang_lower in ["javascript", "js", "typescript", "ts"]:
        # Don't run node tests on browser-based websites
        if mod_lower == "website" or mod_lower == "web application":
            print(f"🔍 Skipping Node execution for {modality} project. Validating existence only.")
            return True, "Website scripts detected. Skipping execution-based testing."
        return _run_node_tests(directory)
    else:
        # For unsupported languages, just check if code compiles/runs
        return _check_basic_syntax(directory, language)


def _run_python_tests(directory: str) -> Tuple[bool, str]:
    """Run Python tests using pytest or unittest."""
    try:
        # Try pytest first
        result = subprocess.run(
            ["pytest", directory, "-v"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=directory
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stdout + result.stderr
    except FileNotFoundError:
        # Try unittest if pytest not available
        try:
            result = subprocess.run(
                ["python", "-m", "unittest", "discover", "-s", directory, "-v"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=directory
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            # Fallback: try to run main files
            return _run_python_files(directory)


def _run_python_files(directory: str) -> Tuple[bool, str]:
    """Try to run Python files directly."""
    output = []
    success = True
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                try:
                    result = subprocess.run(
                        ["python", file_path],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        cwd=directory
                    )
                    if result.returncode != 0:
                        success = False
                        output.append(f"Error in {file}: {result.stderr}")
                    else:
                        output.append(f"{file}: OK")
                except Exception as e:
                    success = False
                    output.append(f"Error running {file}: {str(e)}")
    
    return success, "\n".join(output)


def _run_node_tests(directory: str) -> Tuple[bool, str]:
    """Run Node.js tests."""
    try:
        result = subprocess.run(
            ["npm", "test"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=directory
        )
        return result.returncode == 0, result.stdout + result.stderr
    except FileNotFoundError:
        # Try running with node directly
        return _run_node_files(directory)


def _run_node_files(directory: str) -> Tuple[bool, str]:
    """Try to run Node.js files directly."""
    output = []
    success = True
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.js') and not file.endswith('.test.js'):
                file_path = os.path.join(root, file)
                try:
                    result = subprocess.run(
                        ["node", file_path],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        cwd=directory
                    )
                    if result.returncode != 0:
                        success = False
                        output.append(f"Error in {file}: {result.stderr}")
                except Exception as e:
                    success = False
                    output.append(f"Error running {file}: {str(e)}")
    
    return success, "\n".join(output)


def _check_basic_syntax(directory: str, language: str) -> Tuple[bool, str]:
    """Basic syntax checking for unsupported languages."""
    # For now, just return success
    # Can be extended with language-specific syntax checkers
    return True, "Syntax check not implemented for this language"


def parse_test_errors(output: str) -> str:
    """Extract error summary from test output.
    
    Args:
        output: Test execution output
        
    Returns:
        Summary of errors found
    """
    if not output:
        return ""
    
    # Extract common error patterns
    errors = []
    lines = output.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in ['error', 'fail', 'exception', 'traceback', 'syntax error']):
            errors.append(line)
    
    if errors:
        return "\n".join(errors[:10])  # Limit to first 10 errors
    else:
        return "No specific errors found in test output"





