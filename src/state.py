"""Development state management for the multi-agent system."""

from typing import Dict, Optional


class DevelopmentState:
    """Manages the development state throughout the agent chain."""
    
    def __init__(self):
        super().__init__()
        self.task_prompt: str = ""
        self.modality: str = ""
        self.language: str = ""
        self.codes: Dict[str, str] = {}
        self.review_comments: str = ""
        self.test_reports: str = ""
        self.error_summary: str = ""
        self.project_name: str = ""
        self.output_directory: str = ""
        # Initialize usage tracker
        from src.tools.usage_tracker import UsageTracker
        self.usage_tracker: UsageTracker = UsageTracker()
    
    def update_codes(self, content: str) -> None:
        """Parse and update code files from LLM response.
        
        Args:
            content: LLM response containing code blocks in markdown format
        """
        from src.tools.code_manager import extract_code_blocks
        extracted_codes = extract_code_blocks(content)
        self.codes.update(extracted_codes)
    
    def get_codes_formatted(self) -> str:
        """Format codes for inclusion in prompts.
        
        Returns:
            Formatted string representation of all code files
        """
        from src.tools.code_manager import format_code_for_prompt
        return format_code_for_prompt(self.codes)
    
    def save_to_directory(self, path: Optional[str] = None) -> None:
        """Write all code files to disk.
        
        Args:
            path: Directory path (uses self.output_directory if not provided)
        """
        from src.tools.file_manager import write_files
        directory = path or self.output_directory
        if directory:
            write_files(directory, self.codes)

