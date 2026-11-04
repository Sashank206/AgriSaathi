import os
import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app

client = TestClient(app)

def test_health_check():
    """Verify health endpoint responds with system status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert data["services"]["crop_recommendation"] == "Ready (Environmental & agro-climatic rules active)"

def test_auth_farmer_flow():
    """Verify farmer registration, login, and profile retrieval."""
    test_email = "testfarmer1@agrisaathi.org"
    register_payload = {
        "full_name": "Kisan Ram",
        "email": test_email,
        "password": "securepassword123",
        "phone_number": "9876543210",
        "role": "farmer",
        "village_district": "Ludhiana",
        "state": "Punjab"
    }

    # Register
    res = client.post("/api/auth/register", json=register_payload)
    if res.status_code == 400 and "already exists" in res.text:
        # Existing user, proceed to login
        pass
    else:
        assert res.status_code == 201
        assert "access_token" in res.json()

    # Login
    login_res = client.post("/api/auth/login", json={
        "email": test_email,
        "password": "securepassword123"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    token = login_data["access_token"]
    assert token is not None

    # Get Me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == test_email
    assert me_res.json()["role"] == "farmer"

def test_weather_endpoints():
    """Verify weather current observation and agricultural alerts."""
    res = client.get("/api/weather/current?city=Ludhiana")
    assert res.status_code == 200
    data = res.json()
    assert "current" in data
    assert "alerts" in data
    assert "forecast" in data
    assert data["current"]["temperature_celsius"] is not None

def test_fertilizer_catalog_and_formula():
    """Verify fertilizer catalog retrieval and multi-factor ranking formula."""
    # List products
    res = client.get("/api/fertilizers")
    assert res.status_code == 200
    products = res.json()
    assert len(products) >= 2

    # Compare first two products
    p1 = products[0]["id"]
    p2 = products[1]["id"]
    compare_res = client.post("/api/fertilizers/compare", json={
        "product_ids": [p1, p2],
        "alpha": 0.6
    })
    assert compare_res.status_code == 200
    compare_data = compare_res.json()
    assert "ranked_products" in compare_data
    assert len(compare_data["ranked_products"]) == 2
    assert compare_data["ranked_products"][0]["rank"] == 1
    assert compare_data["alpha_used"] == 0.6

def test_crop_recommendation_no_npk():
    """
    Test crop recommendation based purely on location, soil, water source, and weather.
    Confirms NO manual NPK values are required.
    """
    # Login as farmer first to get token
    login_res = client.post("/api/auth/login", json={
        "email": "testfarmer1@agrisaathi.org",
        "password": "securepassword123"
    })
    token = login_res.json()["access_token"]

    req_payload = {
        "state": "Punjab",
        "district": "Ludhiana",
        "village": "Sahnewal",
        "latitude": 30.9010,
        "longitude": 75.8573,
        "soil_type": "Alluvial Soil",
        "water_source": "Borewell",
        "season": "Rabi (Winter)"
    }

    res = client.post("/api/crop/recommend", json=req_payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["recommendations"]) > 0
    top_crop = data["recommendations"][0]
    assert "crop_name" in top_crop
    assert "suitability_score" in top_crop
    assert "water_requirement" in top_crop

def test_disease_detection_image_validation_and_status():
    """Verify leaf image upload, format validation, and honest unconfigured model response."""
    login_res = client.post("/api/auth/login", json={
        "email": "testfarmer1@agrisaathi.org",
        "password": "securepassword123"
    })
    token = login_res.json()["access_token"]

    # Generate a realistic test in-memory image
    img = Image.new("RGB", (128, 128), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    files = {"file": ("test_leaf.jpg", buf, "image/jpeg")}
    data = {"crop_type": "Tomato"}

    res = client.post(
        "/api/disease/predict",
        files=files,
        data=data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    res_data = res.json()
    assert res_data["success"] is True
    assert res_data["case_id"] is not None
    # Verifies truthful model status handling (model not configured in Phase 1)
    assert res_data["model_configured"] is False
    assert "currently unconfigured in this 40% milestone" in res_data["message"]

def test_role_based_access_control():
    """Verify that a farmer cannot access administrative operations."""
    # Farmer token
    login_res = client.post("/api/auth/login", json={
        "email": "testfarmer1@agrisaathi.org",
        "password": "securepassword123"
    })
    farmer_token = login_res.json()["access_token"]

    # Try accessing admin stats with farmer token -> must be 403 Forbidden
    admin_res = client.get("/api/admin/stats", headers={"Authorization": f"Bearer {farmer_token}"})
    assert admin_res.status_code == 403
    assert "Access forbidden" in admin_res.text

