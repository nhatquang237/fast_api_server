# test/test_main.py
import os
import sys

from pathlib import Path
from fastapi.testclient import TestClient

# Add path to possible import testing code from "src" folder
root_path = Path(__file__).resolve().parents[1]
src_path = os.path.join(root_path, "src")
sys.path.append(src_path)

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/data")
    assert response.status_code == 401
    # assert response.json() == {"message": "Hello, World!"}
