import pytest
from fastapi.testclient import TestClient
from app.main import app
import json
from pathlib import Path

client = TestClient(app)

@pytest.fixture
def sample_evaluation_json():
    return {
        "transcriptions": {
            "model1": [
                {
                    "audio_filepath": "test.wav",
                    "pred_sentence": "테스트 문장입니다."
                }
            ]
        },
        "CER metric": {
            "model1": 0.15
        }
    }

def test_upload_evaluation(sample_evaluation_json):
    """Test evaluation.json upload endpoint"""
    json_str = json.dumps(sample_evaluation_json)
    files = {
        'file': ('evaluation.json', json_str, 'application/json')
    }
    
    response = client.post("/evaluation/upload", files=files)
    assert response.status_code == 200
    assert response.json()["status"] == "success" 