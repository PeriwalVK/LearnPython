import os
from pathlib import Path

# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)
