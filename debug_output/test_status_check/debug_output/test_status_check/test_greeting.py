import unittest
from greeting_cli import greet

class TestGreeting(unittest.TestCase):
    def test_greet(self):
        from io import StringIO
        import sys

        expected_output = "Hello, Alice! Welcome to the CLI tool.\n"
        captured_output = StringIO()
        sys.stdout = captured_output
        greet("Alice")
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()