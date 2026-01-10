"""File system operations for project management."""

import os
from pathlib import Path
from typing import Dict, Optional


def create_project_directory(project_name: str, base_dir: str = "./output") -> str:
    """Create a directory for the project.
    
    Args:
        project_name: Name of the project
        base_dir: Base directory for all projects
        
    Returns:
        Path to the created directory
    """
    project_dir = os.path.join(base_dir, project_name)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir


def write_files(directory: str, codes: Dict[str, str]) -> None:
    """Write code files to disk.
    
    Args:
        directory: Target directory
        codes: Dictionary mapping filename to code content
    """
    os.makedirs(directory, exist_ok=True)
    
    for filename, content in codes.items():
        file_path = os.path.join(directory, filename)
        
        # Create subdirectories if needed
        file_dir = os.path.dirname(file_path)
        if file_dir:
            os.makedirs(file_dir, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)


def read_file(directory: str, filename: str) -> str:
    """Read file content from disk.
    
    Args:
        directory: Directory containing the file
        filename: Name of the file to read
        
    Returns:
        File content as string
    """
    file_path = os.path.join(directory, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()





