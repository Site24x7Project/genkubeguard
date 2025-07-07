import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_endpoint():
    with open("k8s/sample_deployment.yaml", "rb") as f:
        response = client.post("/analyze", files={"file": f})
    assert response.status_code == 200
    data = response.json()
    assert "issues" in data
    assert "explanations" in data
    assert isinstance(data["issues"], list)

def test_patch_endpoint():
    with open("k8s/sample_deployment.yaml", "rb") as f:
        response = client.post("/patch", files={"file": f})
    assert response.status_code == 200
    assert "patched_yaml" in response.json()

def test_suggest_endpoint():
    with open("k8s/sample_deployment.yaml", "rb") as f:
        response = client.post("/suggest", files={"file": f})
    assert response.status_code == 200
    assert "suggestions" in response.json()

def test_suggest_persona_endpoint():
    with open("k8s/sample_deployment.yaml", "rb") as f:
        response = client.post("/suggest-persona?persona=junior", files={"file": f})
    assert response.status_code == 200
    assert "persona_suggestions" in response.json()

def test_memory_endpoint():
    response = client.get("/memory?q=cpu")
    assert response.status_code == 200
    assert "related" in response.json()
