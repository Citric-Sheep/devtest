"""
Script to run the tests for the elevator demand prediction system.
"""

import os
import sys
import pytest

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests():
    """Run the tests for the elevator demand prediction system."""
    # Run the tests
    pytest.main(["-v", "src/tests"])

if __name__ == "__main__":
    run_tests()
