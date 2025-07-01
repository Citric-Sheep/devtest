"""
Script to run the elevator demand prediction system.
"""

import os
import sys
import uvicorn

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_app():
    """Run the elevator demand prediction system."""
    # Run the application
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run_app()
