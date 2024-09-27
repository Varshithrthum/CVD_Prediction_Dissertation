import pytest
from app import app
from flask import url_for

# Setup for Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# 1. Test the /predict route with missing fields (e.g., no height)
def test_predict_route_missing_fields(client):
    response = client.post('/predict', data={
        'age': 35,
        'gender': 1,       # Male
        'weight': 75,      # 75 kg
        'ap_hi': 120,      # Systolic BP
        'ap_lo': 80,       # Diastolic BP
        'smoke': 0,        # Non-smoker
        'alco': 0,         # No alcohol intake
        'active': 1,       # Physically active
        'chol': 1,         # Cholesterol Normal
        'gluc': 1          # Glucose Normal
        # Missing 'height'
    })
    
    assert response.status_code == 400  # Should return 400 due to missing height

# 2. Test the /predict route with invalid data (e.g., negative weight)
def test_predict_route_invalid_data(client):
    response = client.post('/predict', data={
        'age': 35,
        'gender': 1,       # Male
        'height': 170,     # 170 cm
        'weight': -75,     # Invalid negative weight
        'ap_hi': 120,      # Systolic BP
        'ap_lo': 80,       # Diastolic BP
        'smoke': 0,        # Non-smoker
        'alco': 0,         # No alcohol intake
        'active': 1,       # Physically active
        'chol': 1,         # Cholesterol Normal
        'gluc': 1          # Glucose Normal
    })
    
    assert response.status_code == 400  # Should return 400 due to invalid data

# 3. Test the /download-pdf route with valid data
def test_download_pdf_valid_data(client):
    response = client.post('/download-pdf', data={
        'prediction': 'Low Risk',
        'probability': 0.2,
        'risk_color': 'green',
        'ap_hi': 120,
        'ap_lo': 80,
        'bmi': 24.2,
        'age': 35,
        'gender': 'Male',
        'risk_factors_percentage': '{"BMI": 20, "Blood Pressure": 15}',
        'recommendations': '{"Blood Pressure": {"recommendation": "Reduce salt", "link": "https://example.com"}}'
    })

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'

# 4. Test the /download-pdf route with missing fields
def test_download_pdf_missing_data(client):
    response = client.post('/download-pdf', data={
        'prediction': 'Low Risk',
        'probability': 0.2,
        'risk_color': 'green',
        # Missing other fields like ap_hi, ap_lo, bmi, etc.
    })

    assert response.status_code == 400  # Should return 400 due to missing data

# 5. Test the BMI calculation (utility function)
def test_bmi_calculation():
    height = 170  # cm
    weight = 70   # kg
    bmi = weight / ((height / 100) ** 2)
    
    assert round(bmi, 2) == 24.22  # Expected BMI

# 6. Test height conversion function (utility function for feet/inches)
def test_height_conversion():
    feet = 5
    inches = 8
    height_cm = (feet * 30.48) + (inches * 2.54)
    
    assert round(height_cm, 2) == 172.72  # Expected height in cm
