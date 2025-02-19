"""Magnatronic Multi-Agent System Core Module"""

from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

__version__ = '0.1.0'
__author__ = 'Magnatronic Team'