import pytest
from app.model import AIModel
import os
import json

BASELINE_RESPONSES = {
    "test_prompt_1": {
        "expected_keywords": ["2", "4", "equals"],
        "min_length": 5
    },
    "test_prompt_2": {
        "expected_keywords": ["hello"],
        "min_length": 3
    }
}

@pytest.fixture
def model():
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        pytest.skip("CLAUDE_API_KEY not set")
    return AIModel(api_key=api_key)

def test_regression_mathematical(model):
    """Test model produces expected output for math."""
    result = model.generate("What is 2+2?")
    
    # Regression checks
    assert len(result) > 0, "Output should not be empty"
    assert any(keyword in result.lower() for keyword in ["2", "4", "equals"]), \
        f"Output should contain math-related keywords. Got: {result}"

def test_regression_greeting(model):
    """Test model produces greeting output."""
    result = model.generate("Say hello")
    
    assert len(result) >= 3, "Output should be at least 3 chars"
    assert "hello" in result.lower() or "hi" in result.lower(), \
        f"Output should contain greeting. Got: {result}"

def test_regression_consistency(model):
    """Test output consistency between runs."""
    prompt = "Answer: 1+1"
    
    result1 = model.generate_with_metadata(prompt)
    result2 = model.generate_with_metadata(prompt)
    
    # With low temperature, outputs should be identical or very similar
    assert result1["hash"] == result2["hash"], \
        "Model output should be deterministic with low temperature"

def test_no_degradation(model):
    """Test model hasn't degraded."""
    result = model.generate_with_metadata("Test")
    
    # Regression detection: tokens within expected range
    tokens = result["tokens_used"]
    assert 1 <= tokens <= 1000, \
        f"Token count {tokens} outside expected range [1, 1000]"
