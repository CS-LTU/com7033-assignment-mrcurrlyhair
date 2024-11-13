import pytest
from app import app 

# test home page 
def test_landing():
    # Create a test client (flask)
    with app.test_client() as client:
        response = client.get('/')

        # check if theres a html error code 
        assert response.status_code == 200

# test infomation page
def test_information():
    # Create a test client (flask)
    with app.test_client() as client:
        response = client.get('/Information')

        # check if theres a html error code 
        assert response.status_code == 200

# test user info without a signed in account 
def test_user_info():
     # Create a test client (flask)
    with app.test_client() as client:
        response = client.get('/user_info')

        # check if theres a html error code 
        assert response.status_code == 302

# test user


