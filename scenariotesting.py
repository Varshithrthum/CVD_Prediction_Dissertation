import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
def test_successful_prediction_healthy_user(client):
    # Healthy user inputs
    response = client.post('/predict', data={
        'age': 35,
        'gender': 0,  # Female
        'height_cm': 165,
        'weight': 60,
        'ap_hi': 110,  # Systolic BP
        'ap_lo': 70,   # Diastolic BP
        'smoke': 0,    # Non-smoker
        'alco': 0,     # No alcohol
        'active': 1,   # Active
        'chol': 1,     # Normal cholesterol
        'gluc': 1      # Normal glucose
    })
    
    # Check the status code
    assert response.status_code == 200
    
    # Ensure the response contains 'Low Risk' or similar indication
    assert b'Low Risk' in response.data or b'green' in response.data

def test_high_risk_user_with_health_concerns(client):
    # High-risk user inputs
    response = client.post('/predict', data={
        'age': 55,
        'gender': 1,  # Male
        'height_cm': 180,
        'weight': 95,
        'ap_hi': 180,  # Systolic BP
        'ap_lo': 100,  # Diastolic BP
        'smoke': 1,    # Smoker
        'alco': 1,     # Alcohol consumption
        'active': 0,   # Inactive
        'chol': 3,     # Well above normal cholesterol
        'gluc': 3      # Well above normal glucose
    })
    
    # Check the status code
    assert response.status_code == 200
    
    # Ensure the response contains 'High Risk' or similar indication
    assert b'High Risk' in response.data or b'red' in response.data
def test_moderate_risk_user(client):
    # Moderate risk user inputs
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,  # Male
        'height_cm': 175,
        'weight': 80,
        'ap_hi': 140,  # Slightly high systolic BP
        'ap_lo': 90,   # Slightly high diastolic BP
        'smoke': 0,    # Non-smoker
        'alco': 0,     # No alcohol
        'active': 1,   # Active
        'chol': 2,     # Above normal cholesterol
        'gluc': 2      # Above normal glucose
    })

    # Check the status code
    assert response.status_code == 200

    # Ensure the response contains 'Moderate Risk' or similar indication
    assert b'Moderate Risk' in response.data or b'yellow' in response.data
#diffrent sceenarios testing
# 1. Height Scenarios
def test_valid_height_in_cm(client):
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,
        'height_cm': 180,
        'weight': 75,
        'ap_hi': 120,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200

def test_empty_height_field(client):
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,
        'height_cm': '',  # Empty height
        'weight': 75,
        'ap_hi': 120,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 400
   

# 2. Weight Scenarios
def test_valid_weight(client):
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,
        'height_cm': 180,
        'weight': 70,  # Valid weight
        'ap_hi': 120,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200

# 3. Age Scenarios
def test_valid_age(client):
    response = client.post('/predict', data={
        'age': 50,  # Valid age
        'gender': 1,
        'height_cm': 180,
        'weight': 75,
        'ap_hi': 120,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200

    

# 4. Blood Pressure Scenarios
def test_valid_blood_pressure(client):
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,
        'height_cm': 180,
        'weight': 75,
        'ap_hi': 120,  # Valid systolic BP
        'ap_lo': 80,   # Valid diastolic BP
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 200
    

    

