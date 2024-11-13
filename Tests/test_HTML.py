import pytest
from app import app 

def test_landing():
    # Create a test client (flask)
    with app.test_client() as client:
        response = client.get('/')

        # check if theres a html error code 
        assert response.status_code == 200

def test_information():
    # Create a test client (flask)
    with app.test_client() as client:
        response = client.get('/Information')

        # check if theres a html error code 
        assert response.status_code == 200

def test_user_info():
    # Create a test client (flask)
    with app.test_client() as client:
        response = client.get('/user_info')

        # check if theres a html error code 
        assert response.status_code == 200

