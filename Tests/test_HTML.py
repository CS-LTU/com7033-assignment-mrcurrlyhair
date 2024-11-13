import pytest
import pymongo 
import sqlite3
from app import app, user_collection, get_sqlite_connection
from Mongo_Loader import hashing_pass

# Mongo setup to create a test user
def create_testuser_mongo():

    # Testuser details
    test_username = "testuser"
    test_password = "Churchill!2"
    hashed_password = hashing_pass(test_password)

    # Creating Testuser
    test_user = {
        "u_id": 2,  # no user uses id of 1 , unique to testuser 
        "u_username": test_username,
        "u_password": hashed_password,
        "is_admin": False
    }

    # Adding testuser to Mogno
    user_collection.insert_one(test_user)
    print("Testuser created")

def delete_testuser_mongo():
    # Removes the test user with a specific u_id
    user_collection.delete_one({"u_id": 2})
    print("Testuser deleted")


# SPACE FOR SQL 
























# fixture that runs start_and_delete_Testuser once.
@pytest.fixture(scope="session", autouse=True)

# Function to create then delete testuser, in Mongo and SQL,fter tests 
def start_and_delete_Testuser():
    # Runs the function to create test user in Mogno
    create_testuser_mongo()

    # Runs the function to create testuser in SQL    

    
    # Allows tests to run while testuser is in Mongo and SQL
    yield  

    # Runs the function to delete testuser in Mongo 
    delete_testuser_mongo()

    # Runs the function to delete testuser in SQL

# Fixture to create the function of cleint reusable while testing
@pytest.fixture
# Creates test client ( for flask html )
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test home page 
def test_landing(client):
    # Loads home html
    response = client.get('/')
    # Check if theres a html error code, 200 is ok 
    assert response.status_code == 200

# Test infomation page
def test_information(client):
    # Loads infomation html
    response = client.get('/Information')
    # Check if theres a html error code, 200 is ok 
    assert response.status_code == 200

# Test login page 
def test_login(client):
    # Login for testuser to be sent in the login form
    login_data = {
        'username': 'testuser',
        'password': 'Churchill!2'
    }

    # Emulates login 
    response = client.post('/Login', data=login_data)

    # Check if redirected to user_info and have a html code of 302
    assert response.status_code == 302 
    assert response.headers['Location'] == '/user_info'  


# Test user info without a signed in account 
def test_user_info(client):
    # Loads user html
    response= client.get('/user_info')
    # HTML code 302 should appear as no account is signed in (redirect to login)
    assert response.status_code == 302
    assert response.headers['Location'] == '/Login' 

# Test user info while signed in 
def test_user_info_sign(client):
    # Login for testuser to be sent in the login form
    login_data = {
        'username': 'testuser',
        'password': 'Churchill!2'
    }

    # Emulates login 
    response = client.post('/Login', data=login_data, follow_redirects=True)

    # Opens user_info page
    response = client.get('/user_info')

    # Check if user info has loaded correclty
    assert response.status_code == 200

    # Reads if user id is 2 from form
    assert b"<strong>User ID:</strong> 2" in response.data



    








