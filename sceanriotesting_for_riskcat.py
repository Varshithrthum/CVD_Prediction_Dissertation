import pytest
from app import app  # Import your Flask app here

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test cases for Low Risk (valid values only)
def test_low_risk_prediction_1(client):
    response = client.post('/predict', data={
        'age': 30,
        'gender': 1,  # Male
        'height_cm': 175,
        'weight': 65,
        'ap_hi': 110,
        'ap_lo': 70,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,  # Cholesterol Normal
        'gluc': 1   # Glucose Normal
    })
    assert response.status_code == 200
    assert b"Low Risk" in response.data

def test_low_risk_prediction_2(client):
    response = client.post('/predict', data={
        'age': 35,
        'gender': 2,  # Female
        'height_cm': 160,
        'weight': 55,
        'ap_hi': 115,
        'ap_lo': 75,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200
    assert b"Low Risk" in response.data

def test_low_risk_prediction_3(client):
    response = client.post('/predict', data={
        'age': 32,
        'gender': 1,  # Male
        'height_cm': 180,
        'weight': 70,
        'ap_hi': 115,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200
    assert b"Low Risk" in response.data

def test_low_risk_prediction_4(client):
    response = client.post('/predict', data={
        'age': 31,
        'gender': 2,  # Female
        'height_cm': 170,
        'weight': 65,
        'ap_hi': 110,
        'ap_lo': 70,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200
    assert b"Low Risk" in response.data

def test_low_risk_prediction_5(client):
    response = client.post('/predict', data={
        'age': 28,
        'gender': 1,  # Male
        'height_cm': 175,
        'weight': 60,
        'ap_hi': 105,
        'ap_lo': 65,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200
    assert b"Low Risk" in response.data

# Test cases for Moderate Risk (valid values only)
def test_moderate_risk_prediction_1(client):
    response = client.post('/predict', data={
        'age': 50,
        'gender': 1,  # Male
        'height_cm': 170,
        'weight': 75,
        'ap_hi': 135,
        'ap_lo': 85,
        'smoke': 1,
        'alco': 1,
        'active': 0,
        'chol': 2,  # Cholesterol Above Normal
        'gluc': 2   # Glucose Above Normal
    })
    assert response.status_code == 200
    assert b"Moderate Risk" in response.data

def test_moderate_risk_prediction_2(client):
    response = client.post('/predict', data={
        'age': 48,
        'gender': 2,  # Female
        'height_cm': 160,
        'weight': 70,
        'ap_hi': 140,
        'ap_lo': 90,
        'smoke': 1,
        'alco': 0,
        'active': 0,
        'chol': 2,
        'gluc': 2
    })
    assert response.status_code == 200
    assert b"Moderate Risk" in response.data

def test_moderate_risk_prediction_3(client):
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,  # Male
        'height_cm': 175,
        'weight': 80,
        'ap_hi': 130,
        'ap_lo': 85,
        'smoke': 1,
        'alco': 1,
        'active': 0,
        'chol': 2,
        'gluc': 2
    })
    assert response.status_code == 200
    assert b"Moderate Risk" in response.data

def test_moderate_risk_prediction_4(client):
    response = client.post('/predict', data={
        'age': 52,
        'gender': 2,  # Female
        'height_cm': 165,
        'weight': 75,
        'ap_hi': 135,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 1,
        'active': 0,
        'chol': 2,
        'gluc': 2
    })
    assert response.status_code == 200
    assert b"Moderate Risk" in response.data

def test_moderate_risk_prediction_5(client):
    response = client.post('/predict', data={
        'age': 53,
        'gender': 1,  # Male
        'height_cm': 180,
        'weight': 85,
        'ap_hi': 135,
        'ap_lo': 85,
        'smoke': 1,
        'alco': 0,
        'active': 0,
        'chol': 2,
        'gluc': 2
    })
    assert response.status_code == 200
    assert b"Moderate Risk" in response.data

# Test cases for High Risk (valid values only)
def test_high_risk_prediction_1(client):
    response = client.post('/predict', data={
        'age': 60,
        'gender': 1,  # Male
        'height_cm': 165,
        'weight': 100,
        'ap_hi': 180,
        'ap_lo': 120,
        'smoke': 1,
        'alco': 1,
        'active': 0,
        'chol': 3,  # Cholesterol Well Above Normal
        'gluc': 3   # Glucose Well Above Normal
    })
    assert response.status_code == 200
    assert b"High Risk" in response.data

def test_high_risk_prediction_2(client):
    response = client.post('/predict', data={
        'age': 65,
        'gender': 2,  # Female
        'height_cm': 160,
        'weight': 95,
        'ap_hi': 175,
        'ap_lo': 110,
        'smoke': 1,
        'alco': 1,
        'active': 0,
        'chol': 3,
        'gluc': 3
    })
    assert response.status_code == 200
    assert b"High Risk" in response.data

