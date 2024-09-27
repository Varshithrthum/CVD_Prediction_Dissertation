import pytest
from app import app

# This will use pytest-flask to create a test client for the Flask app.
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_valid_submission_with_centimeters(client):
    response = client.post('/predict', data={
        'age': 50,
        'gender': 1,
        'height_cm': 175,
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
    assert b'Prediction Result' in response.data

def test_incomplete_input_data(client):
    response = client.post('/predict', data={
        'age': 50,
        'gender': 1,
        # Missing height, weight, and other fields
        'ap_hi': 130,
        'ap_lo': 85
    })

    # Assert that the response indicates missing input fields and returns a 400 status
    assert response.status_code == 400
    assert b'Missing required input fields' in response.data



def test_missing_required_fields(client):
    response = client.post('/predict', data={
        'age': '',
        'gender': 1,
        'height_cm': 175,
        'weight': '',
        'ap_hi': 120,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })
    assert response.status_code == 400
    assert b'Missing required input fields' in response.data
def test_pdf_generation(client):
    # First, submit valid prediction data
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,
        'height_cm': 175,
        'weight': 70,
        'ap_hi': 120,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })

    # After prediction, submit a request for the PDF generation
    pdf_response = client.post('/download-pdf', data={
        'prediction': 'Low Risk',
        'probability': 0.2,
        'risk_color': 'green',
        'ap_hi': 120,
        'ap_lo': 80,
        'bmi': 22.86,
        'age': 45,
        'gender': 'Male',
        'risk_factors_percentage': '{"BMI": 30, "Cholesterol": 20}',
        'recommendations': '{"BMI": {"recommendation": "Maintain a healthy weight"}}'
    })

    # Assert that the PDF generation is successful (check for status 200 and PDF content type)
    assert pdf_response.status_code == 200
    assert pdf_response.headers['Content-Type'] == 'application/pdf'
def test_invalid_bmi_calculation(client):
    response = client.post('/predict', data={
        'age': 45,
        'gender': 1,  # Male
        'height_cm': 0,  # Zero height should not be allowed, will lead to invalid BMI
        'weight': 85,
        'ap_hi': 120,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 1,
        'gluc': 1
    })

    # Assert that the response indicates invalid BMI or input values (status 400 or custom error message)
    assert response.status_code == 400
    
def test_invalid_data_submission(client):
    response = client.post('/predict', data={
        'age': 30,
        'gender': 1,  # Male
        'height_cm': -150,  # Invalid negative height
        'weight': 70,
        'ap_hi': 120,
        'ap_lo': 80,
        'smoke': 0,
        'alco': 0,
        'active': 1,
        'chol': 2,
        'gluc': 1
    })

    # Assert that the response indicates invalid data (status 400 or custom error message)
    assert response.status_code == 400
    
