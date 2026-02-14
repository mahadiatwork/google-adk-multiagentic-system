"""Code extraction and formatting utilities."""

import re
from typing import Dict


def extract_code_blocks(text: str) -> Dict[str, str]:
    """Extract code blocks from markdown-formatted text.
    
    Expected format:
    FILENAME
    ```LANGUAGE
    CODE
    ```
    
    Args:
        text: Text containing markdown code blocks
        
    Returns:
        Dictionary mapping filename to code content
    """
    codes = {}
    
    # Pattern to match: filename (optional) followed by code block
    # Matches: FILENAME\n```LANGUAGE\nCODE\n```
    pattern = r'(?:^|\n)([A-Za-z0-9_\-\.\/]+\.(?:py|js|ts|java|cpp|c|html|css|json|yaml|yml|md|txt|sh|bat|ps1))(?:\n|$)(?:```(?:python|javascript|typescript|java|cpp|c|html|css|json|yaml|bash|shell|powershell|plaintext)?\n(.*?)```|```\n(.*?)```)'
    
    # Try more flexible line-by-line parsing
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if line looks like a filename indicator
        # Support matches like: "index.html", "FILENAME: index.html", "File: index.html", "## index.html"
        clean_line = line
        prefixes_to_strip = ["FILENAME:", "File:", "Filename:", "##", "**"]
        for prefix in prefixes_to_strip:
            if clean_line.upper().startswith(prefix.upper()):
                clean_line = clean_line[len(prefix):].strip()
        
        clean_line = clean_line.strip("*#: ")
        
        # Stricter filename validation
        # 1. Must contain a dot and a valid extension
        # 2. Must be relatively short (< 100 chars)
        # 3. Must NOT contain spaces
        # 4. Must NOT start with common sentence words
        valid_extensions = ('.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.html', '.css', '.json', '.yaml', '.yml', '.md', '.sh', '.bat', '.ps1', '.txt')
        
        is_potential_filename = (
            clean_line and 
            not clean_line.startswith('```') and
            any(clean_line.lower().endswith(ext) for ext in valid_extensions) and
            ' ' not in clean_line and
            len(clean_line) < 100
        )
        
        if is_potential_filename:
            # Potential filename
            filename = clean_line
            # Remove any characters invalid for filenames (especially :)
            filename = re.sub(r'[:*?"<>|]', '', filename)
            
            # Look for code block starting on next non-empty line
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            
            if j < len(lines) and lines[j].strip().startswith('```'):
                # Found code block
                code_lines = []
                j += 1
                
                # Collect code until closing ```
                while j < len(lines):
                    if lines[j].strip() == '```':
                        break
                    code_lines.append(lines[j])
                    j += 1
                
                if code_lines:
                    codes[filename] = '\n'.join(code_lines)
                    i = j
        i += 1
    
    # Fallback: extract any code blocks with language hints
    if not codes:
        # Pattern: ```language\ncode\n```
        code_block_pattern = r'```(?:python|javascript|typescript|java|cpp|c|html|css|json|yaml|bash|shell|plaintext)?\n(.*?)```'
        matches = re.finditer(code_block_pattern, text, re.DOTALL)
        for idx, match in enumerate(matches):
            code = match.group(1).strip()
            if code:
                # Try to infer filename from context or use default
                filename = f"file_{idx + 1}.py"  # Default to Python
                codes[filename] = code
    
    return codes


def format_code_for_prompt(codes: Dict[str, str]) -> str:
    """Format code dictionary for inclusion in LLM prompts.
    
    Args:
        codes: Dictionary mapping filename to code content
        
    Returns:
        Formatted string representation
    """
    if not codes:
        return "No code files available."
    
    formatted = []
    for filename, content in codes.items():
        formatted.append(f"{filename}")
        formatted.append("```")
        formatted.append(content)
        formatted.append("```")
        formatted.append("")
    
    return "\n".join(formatted)


def validate_code_structure(codes: Dict[str, str]) -> bool:
    """Validate that code structure is reasonable.
    
    Args:
        codes: Dictionary mapping filename to code content
        
    Returns:
        True if structure is valid, False otherwise
    """
    if not codes:
        return False
    
    # Basic validation: check for non-empty files
    for filename, content in codes.items():
        if not content or not content.strip():
            return False
    
    return True





