"""Basic flow tests for the multi-agent system."""

import os
import sys
import unittest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.state import DevelopmentState
from src.tools.code_manager import extract_code_blocks, format_code_for_prompt
from src.tools.file_manager import create_project_directory, write_files


class TestBasicFlow(unittest.TestCase):
    """Test basic functionality of the system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_output_dir = "./test_output"
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def tearDown(self):
        """Clean up after tests."""
        import shutil
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
    
    def test_state_initialization(self):
        """Test DevelopmentState initialization."""
        state = DevelopmentState()
        self.assertEqual(state.task_prompt, "")
        self.assertEqual(state.modality, "")
        self.assertEqual(state.codes, {})
    
    def test_code_extraction(self):
        """Test code block extraction."""
        text = """
        main.py
        ```python
        print("Hello, World!")
        ```
        """
        codes = extract_code_blocks(text)
        self.assertIn("main.py", codes)
        self.assertIn("print", codes["main.py"])
    
    def test_code_formatting(self):
        """Test code formatting for prompts."""
        codes = {
            "main.py": "print('Hello')",
            "test.py": "def test(): pass"
        }
        formatted = format_code_for_prompt(codes)
        self.assertIn("main.py", formatted)
        self.assertIn("print", formatted)
        self.assertIn("test.py", formatted)
    
    def test_file_operations(self):
        """Test file creation and writing."""
        project_dir = create_project_directory("test_project", self.test_output_dir)
        self.assertTrue(os.path.exists(project_dir))
        
        codes = {
            "main.py": "print('Hello')"
        }
        write_files(project_dir, codes)
        
        main_file = os.path.join(project_dir, "main.py")
        self.assertTrue(os.path.exists(main_file))
        
        with open(main_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, "print('Hello')")


if __name__ == "__main__":
    unittest.main()





