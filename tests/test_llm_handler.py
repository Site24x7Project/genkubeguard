import pytest
from src import llm_handler

sample_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-deployment
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: test-container
        image: nginx
"""

def test_explain_should_be_specific():
    explanation = llm_handler.explain("Container is using an invalid image tag")
    assert isinstance(explanation, str)
    assert "image" in explanation.lower()
    assert any(word in explanation.lower() for word in ["recommend", "suggest", "advise"])


def test_generate_patch_should_add_security():
    patch = llm_handler.generate_patch(sample_yaml)
    assert isinstance(patch, str)
    assert "readOnlyRootFilesystem" in patch
    assert "runAsNonRoot" in patch
    assert any(word in patch for word in ["resources", "cpu", "memory", "limits"]), "Resources block missing"

def test_suggest_should_provide_tips():
    suggestions = llm_handler.suggest(sample_yaml)
    assert isinstance(suggestions, str)
    assert any(phrase in suggestions.lower() for phrase in ["consider", "recommend", "security improvement", "you should"])


def test_persona_suggestion_junior_style():
    result = llm_handler.suggest_with_persona(sample_yaml, persona="junior")
    assert isinstance(result, str)
    assert "hi there" in result.lower()
    assert "let's make this yaml even better" in result.lower()
