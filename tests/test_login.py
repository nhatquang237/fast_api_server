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

test_data = {
    "username": "teo",
    "password": "quang123"
}

def test_register():
    response = client.post("/register", json=test_data)
    assert response.status_code == 200
    assert isinstance(response.json(), str)

def test_dulicate_register():
    response = client.post("/register", json=test_data)
    assert response.status_code == 400
    assert response.json() in (None, 'None')

def test_login():
    response = client.post("/login", data=test_data)
    result = response.json()
    assert response.status_code == 200
    assert result["access_token"] is not None
    assert result["token_type"] == "bearer"

def test_username_check():
    response = client.post("/check", json=test_data)
    assert response.status_code == 200
    assert response.json() is True
