"""Phase-specific prompts for the development workflow."""

DEMAND_ANALYSIS_PROMPT = """Analyze the following task and determine the product modality:

Task: {task_prompt}

Please analyze the requirements and determine what type of product this should be.
Respond with the modality in the format: <INFO>MODALITY</INFO>

Examples:
- For a web application: <INFO>Website</INFO>
- For a desktop application: <INFO>Application</INFO>
- For a game: <INFO>Game</INFO>
- For a command-line tool: <INFO>CLI Tool</INFO>
"""

LANGUAGE_SELECTION_PROMPT = """Based on the task and product modality, select the appropriate programming language:

Task: {task_prompt}
Modality: {modality}

Select the best programming language for this project.
Respond with: <INFO>LANGUAGE</INFO>

Examples: Python, JavaScript, Java, C++, etc.
"""

CODING_PROMPT = """Write the code for the following task:

Task: {task_prompt}
Modality: {modality}
Language: {language}

Please write complete, runnable code. Use the following format for each file:

FILENAME
```LANGUAGE
CODE_CONTENT
```

Ensure the code is well-structured, documented, and follows best practices.
"""

CODE_REVIEW_PROMPT = """Review the following code:

Task: {task_prompt}
Language: {language}

Current Code:
{codes}

Please review the code for:
1. Code quality and readability
2. Potential bugs or issues
3. Best practices adherence
4. Completeness

If the code is satisfactory, respond with: <INFO>Finished</INFO>
Otherwise, provide specific feedback on what needs to be improved.
"""

TESTING_PROMPT = """Analyze the test results and identify any issues:

Task: {task_prompt}
Language: {language}

Test Results:
{test_reports}

Errors:
{error_summary}

Current Code:
{codes}

Please analyze the test output and errors. Identify the root causes and suggest fixes.
If no errors are found, respond with: <INFO>No errors</INFO>
Otherwise, provide a detailed analysis of the issues.
"""

FIX_CODE_PROMPT = """Fix the code based on the following feedback:

Task: {task_prompt}
Language: {language}

Feedback:
{feedback}

Current Code:
{codes}

Please fix the issues and provide the corrected code in the same format:
FILENAME
```LANGUAGE
CODE_CONTENT
```
"""





