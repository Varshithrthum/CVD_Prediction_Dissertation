import pytest
from app import app  # Import your Flask app here

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test cases to ensure bias-free predictions across gender and age

# Low Risk Prediction Tests (Bias Testing for Gender and Age)
def test_low_risk_young_male(client):
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
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200
    assert b"Low Risk" in response.data

def test_low_risk_young_female(client):
    response = client.post('/predict', data={
        'age': 30,
        'gender': 2,  # Female
        'height_cm': 165,
        'weight': 60,
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

def test_low_risk_middle_aged_male(client):
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,  # Male
        'height_cm': 180,
        'weight': 75,
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

def test_low_risk_middle_aged_female(client):
    response = client.post('/predict', data={
        'age': 45,
        'gender': 2,  # Female
        'height_cm': 160,
        'weight': 65,
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

# Moderate Risk Prediction Tests (Bias Testing for Gender and Age)
def test_moderate_risk_older_male(client):
    response = client.post('/predict', data={
        'age': 55,
        'gender': 1,  # Male
        'height_cm': 170,
        'weight': 85,
        'ap_hi': 135,
        'ap_lo': 85,
        'smoke': 1,
        'alco': 1,
        'active': 0,
        'chol': 2,
        'gluc': 2
    })
    assert response.status_code == 200
    assert b"Moderate Risk" in response.data

def test_moderate_risk_older_female(client):
    response = client.post('/predict', data={
        'age': 55,
        'gender': 2,  # Female
        'height_cm': 165,
        'weight': 75,
        'ap_hi': 135,
        'ap_lo': 85,
        'smoke': 1,
        'alco': 1,
        'active': 0,
        'chol': 2,
        'gluc': 2
    })
    assert response.status_code == 200
    assert b"Moderate Risk" in response.data

def test_moderate_risk_young_male(client):
    response = client.post('/predict', data={
        'age': 40,
        'gender': 1,  # Male
        'height_cm': 180,
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