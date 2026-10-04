import anthropic
import json
import hashlib

class AIModel:
    """AI model with reproducible output for regression testing."""
    
    def __init__(self, api_key: str, model: str = "claude-opus-4-1"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.1  # Low for reproducibility
    
    def generate(self, prompt: str) -> str:
        """Generate content using Claude."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def generate_with_metadata(self, prompt: str) -> dict:
        """Generate content and return with metadata."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        output_hash = hashlib.sha256(content.encode()).hexdigest()
        
        return {
            "content": content,
            "model": self.model,
            "tokens_used": response.usage.output_tokens,
            "hash": output_hash
        }
    
    def health_check(self) -> bool:
        """Check if model is working."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Say 'ok'"}]
            )
            return message.content[0].text.lower() == "ok"
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
