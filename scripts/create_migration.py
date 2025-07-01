"""
Script to create a new Alembic migration.
"""

import os
import sys
import subprocess
import argparse

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_migration(message):
    """Create a new Alembic migration."""
    # Create the migration
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new Alembic migration.")
    parser.add_argument("message", help="Migration message")
    args = parser.parse_args()
    
    create_migration(args.message)
