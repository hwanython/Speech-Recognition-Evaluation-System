import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """Test main page loads correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert "markdown-content" in response.text

def test_evaluation_page():
    """Test evaluation page loads correctly"""
    response = client.get("/evaluation")
    assert response.status_code == 200
    assert "drop-zone" in response.text

def test_dataset_page():
    """Test dataset page loads correctly"""
    response = client.get("/dataset")
    assert response.status_code == 200
    assert "dataset-sections" in response.text 