import time
import pytest
from app import app

# This will use pytest-flask to create a test client for the Flask app.
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
# Test performance for valid prediction request
def test_predict_route_performance(client):
    start_time = time.time()
    
    response = client.post('/predict', data={
        'age': 45,
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
    
    # Measure the response time
    end_time = time.time()
    response_time = end_time - start_time
    
    # Ensure response is successful
    assert response.status_code == 200
    
    # Assert that the response time is within an acceptable range (e.g., less than 1 second)
    assert response_time < 1, f"Response time exceeded 1 second: {response_time} seconds"
def test_predict_route_load(client):
    max_requests = 100  # Number of requests to simulate
    response_times = []
    
    for _ in range(max_requests):
        start_time = time.time()
        
        response = client.post('/predict', data={
            'age': 45,
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
        
        # Measure the response time
        end_time = time.time()
        response_times.append(end_time - start_time)
        
        # Ensure each response is successful
        assert response.status_code == 200
    
    # Calculate the average response time
    average_response_time = sum(response_times) / len(response_times)
    
    # Assert that the average response time remains within a reasonable range
    assert average_response_time < 1, f"Average response time exceeded 1 second: {average_response_time} seconds"
