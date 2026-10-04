#!/usr/bin/env python3
"""AI-Enabled Application with Flask API."""

import os
from flask import Flask, request, jsonify
from app.model import AIModel
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize model
api_key = os.getenv("CLAUDE_API_KEY", "")
model = AIModel(api_key=api_key)

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    is_healthy = model.health_check()
    return jsonify({
        "status": "healthy" if is_healthy else "unhealthy",
        "model": model.model
    }), 200 if is_healthy else 503

@app.route("/generate", methods=["POST"])
def generate():
    """Generate content endpoint."""
    data = request.json
    
    if not data or "prompt" not in data:
        return jsonify({"error": "prompt is required"}), 400
    
    try:
        result = model.generate_with_metadata(data["prompt"])
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    """API info endpoint."""
    return jsonify({
        "name": "AI Application",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "generate": "POST /generate"
        }
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
