import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from pathlib import Path

client = TestClient(app)

def test_get_raw_dataset():
    """Test raw dataset details endpoint"""
    response = client.get("/dataset/raw/eval_v1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "file_count" in data

def test_get_processed_dataset():
    """Test processed dataset details endpoint"""
    response = client.get("/dataset/processed/dataset_v1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "file_count" in data
    assert "has_dataset_json" in data 