# backend/tests/conftest.py
import sys
from pathlib import Path

# project root = the directory that contains "app"
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))