import pytest
from app.model import AIModel
import os

@pytest.fixture
def model():
    api_key = os.getenv("CLAUDE_API_KEY", "test-key")
    return AIModel(api_key=api_key)

def test_model_initialization(model):
    """Test model initializes correctly."""
    assert model.model == "claude-opus-4-1"
    assert model.temperature == 0.1

def test_generate_returns_string(model):
    """Test generate returns a string."""
    if not os.getenv("CLAUDE_API_KEY"):
        pytest.skip("CLAUDE_API_KEY not set")
    
    result = model.generate("What is 2+2?")
    assert isinstance(result, str)
    assert len(result) > 0

def test_metadata_generation(model):
    """Test metadata is generated correctly."""
    if not os.getenv("CLAUDE_API_KEY"):
        pytest.skip("CLAUDE_API_KEY not set")
    
    result = model.generate_with_metadata("Say hello")
    assert "content" in result
    assert "hash" in result
    assert "tokens_used" in result
    assert len(result["hash"]) == 64  # SHA256

def test_health_check():
    """Test health check endpoint works."""
    if not os.getenv("CLAUDE_API_KEY"):
        pytest.skip("CLAUDE_API_KEY not set")
    
    model = AIModel(api_key=os.getenv("CLAUDE_API_KEY"))
    assert isinstance(model.health_check(), bool)
