import pytest
from fastapi.testclient import TestClient
from app.main import app

# Initialize the test client
client = TestClient(app)

# Mock data for testing
mock_campaign_request = {
    "campaign_name": "Launch Campaign",
    "target_audience": "Tech Enthusiasts",
    "content_type": "Blog Post",
    "keywords": ["AI", "automation", "marketing"],
    "tone": "Professional",
    "length": 500
}

mock_campaign_response = {
    "campaign_name": "Launch Campaign",
    "content": "Introducing our latest AI-driven automation tools for marketing. Discover how AI can revolutionize your campaigns with efficiency and precision...",
    "status": "success"
}

mock_error_response = {
    "detail": "Invalid input data"
}

# Test cases
def test_health_check():
    """
    Test the health check route to ensure the API is running.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_content_success():
    """
    Test the /generate-content route with valid input data.
    """
    response = client.post("/generate-content", json=mock_campaign_request)
    assert response.status_code == 200
    assert "campaign_name" in response.json()
    assert "content" in response.json()
    assert response.json()["campaign_name"] == mock_campaign_request["campaign_name"]

def test_generate_content_invalid_input():
    """
    Test the /generate-content route with invalid input data.
    """
    invalid_request = {
        "campaign_name": "",
        "target_audience": "",
        "content_type": "",
        "keywords": [],
        "tone": "",
        "length": -1
    }
    response = client.post("/generate-content", json=invalid_request)
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

def test_generate_content_large_request():
    """
    Test the /generate-content route with a large dataset.
    """
    large_request = {
        "campaign_name": "Massive Campaign",
        "target_audience": "Global Audience",
        "content_type": "Social Media Posts",
        "keywords": ["AI", "automation", "marketing", "global", "reach", "engagement", "strategy", "branding"] * 100,
        "tone": "Casual",
        "length": 10000
    }
    response = client.post("/generate-content", json=large_request)
    assert response.status_code == 200
    assert "campaign_name" in response.json()
    assert "content" in response.json()
    assert len(response.json()["content"]) > 0

def test_generate_content_missing_fields():
    """
    Test the /generate-content route with missing fields in the request.
    """
    incomplete_request = {
        "campaign_name": "Incomplete Campaign",
        "target_audience": "Tech Enthusiasts"
        # Missing other required fields
    }
    response = client.post("/generate-content", json=incomplete_request)
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

def test_generate_content_unsupported_content_type():
    """
    Test the /generate-content route with an unsupported content type.
    """
    unsupported_request = {
        "campaign_name": "Unsupported Campaign",
        "target_audience": "Tech Enthusiasts",
        "content_type": "UnknownType",
        "keywords": ["AI", "automation"],
        "tone": "Professional",
        "length": 500
    }
    response = client.post("/generate-content", json=unsupported_request)
    assert response.status_code == 400  # Bad Request
    assert response.json() == mock_error_response

def test_generate_content_edge_case_length():
    """
    Test the /generate-content route with edge case for length (e.g., 0 or extremely high).
    """
    edge_case_request = {
        "campaign_name": "Edge Case Campaign",
        "target_audience": "Tech Enthusiasts",
        "content_type": "Blog Post",
        "keywords": ["AI", "automation"],
        "tone": "Professional",
        "length": 0  # Edge case for length
    }
    response = client.post("/generate-content", json=edge_case_request)
    assert response.status_code == 400  # Bad Request
    assert response.json() == mock_error_response