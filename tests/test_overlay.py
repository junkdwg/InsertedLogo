"""Tests for overlay endpoints"""

import pytest
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())


def test_overlay_missing_auth():
    """Test overlay endpoint without bearer token"""
    payload = {
        "image_url": "https://example.com/image.jpg",
        "logo_url": "https://example.com/logo.png"
    }
    response = client.post("/api/overlay-logo", json=payload)
    assert response.status_code == 401  # Unauthorized without auth header


def test_overlay_invalid_token():
    """Test overlay endpoint with invalid bearer token"""
    payload = {
        "image_url": "https://example.com/image.jpg",
        "logo_url": "https://example.com/logo.png"
    }
    response = client.post(
        "/api/overlay-logo",
        json=payload,
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401  # Unauthorized


def test_overlay_invalid_url():
    """Test overlay endpoint with invalid image URL"""
    payload = {
        "image_url": "https://invalid.example.com/not-exist.jpg",
        "logo_url": "https://invalid.example.com/not-exist.png"
    }
    # Note: Would fail with 400 if trying to fetch from non-existent URL
    # Requires proper bearer token to test
