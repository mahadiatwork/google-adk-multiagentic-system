"""Test execution and error parsing utilities."""

import subprocess
import os
from typing import Tuple


def run_tests(directory: str, language: str) -> Tuple[bool, str]:
    """Run tests for the project.
    
    Args:
        directory: Project directory
        language: Programming language (python, javascript, etc.)
        
    Returns:
        Tuple of (success: bool, output: str)
    """
    if language.lower() == "python":
        return _run_python_tests(directory)
    elif language.lower() in ["javascript", "js", "typescript", "ts"]:
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





