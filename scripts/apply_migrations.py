"""
Script to apply Alembic migrations.
"""

import os
import sys
import subprocess
import argparse

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def apply_migrations(revision="head"):
    """Apply Alembic migrations."""
    # Apply the migrations
    subprocess.run(["alembic", "upgrade", revision])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Alembic migrations.")
    parser.add_argument("--revision", default="head", help="Revision to upgrade to (default: head)")
    args = parser.parse_args()
    
    apply_migrations(args.revision)
