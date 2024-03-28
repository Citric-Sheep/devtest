"""
Main file. This file is run in the entrypoint. 
"""

from server import app
from dotenv import load_dotenv
import os


load_dotenv()


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))  # True for dev instances, for production should be False.
