# tests/conftest.py
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the project directory to the Python path
import sys
import os

sys.path.append("..")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
