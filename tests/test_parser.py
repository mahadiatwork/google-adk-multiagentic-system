import unittest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.code_manager import extract_code_block

class TestCodeExtraction(unittest.TestCase):
    def test_standard_markdown(self):
        llm_output = 'Here is your code:\n```python\nimport sys\nprint("hello")\n```\nGood luck!'
        expected = 'import sys\nprint("hello")'
        self.assertEqual(extract_code_block(llm_output), expected)

    def test_naked_code(self):
        llm_output = 'import sys\nprint("hello")'
        expected = 'import sys\nprint("hello")'
        self.assertEqual(extract_code_block(llm_output), expected)

    def test_case_insensitivity(self):
        llm_output = '```PYTHON\nprint("test")\n```'
        expected = 'print("test")'
        self.assertEqual(extract_code_block(llm_output), expected)

    def test_no_language_label(self):
        llm_output = '```\nprint("test")\n```'
        expected = 'print("test")'
        self.assertEqual(extract_code_block(llm_output), expected)

    def test_multiline_strings(self):
        llm_output = '```python\ncode = """\nmultiline\n"""\n```'
        expected = 'code = """\nmultiline\n"""'
        self.assertEqual(extract_code_block(llm_output), expected)

if __name__ == "__main__":
    unittest.main()
