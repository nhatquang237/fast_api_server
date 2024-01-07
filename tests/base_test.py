import os
import sys

from pathlib import Path
from fastapi.testclient import TestClient

# Add path to possible import testing code from "src" folder
root_path = Path(__file__).resolve().parents[1]
src_path = os.path.join(root_path, "src")
sys.path.append(src_path)

from main import app


class TestBase:
    client = TestClient(app)
