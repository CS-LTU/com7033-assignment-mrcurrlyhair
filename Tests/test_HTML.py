import pytest
import pymongo 
from app import app
from Mongo_Loader import hashing_pass 


# MongoDB setup to create a test user
def create_testuser():
    #Connect to Mongo
    mdb_path = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mdb_path)
    db = client["medicalDB"]
    user_collection = db["user"]

    # Testuser details
    test_username = "testuser"
    test_password = "Churchill!2"
    hashed_password = hashing_pass(test_password)

    # Creating Testuser
    test_user = {
        "u_id": 2,  # Unique ID for test user
        "u_username": test_username,
        "u_password": hashed_password,
        "is_admin": False
    }

    # Adding testuser to mogno
    user_collection.insert_one(test_user)
    print("Test user created")


#allows client to be reused 
@pytest.fixture
#Creates test client ( for flask html )
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# test home page 
def test_landing(client):
    # loads home html
    response = client.get('/')
    # check if theres a html error code, 200 is ok 
    assert response.status_code == 200

# test infomation page
def test_information(client):
    # loads infomation html
    response = client.get('/Information')
    # check if theres a html error code, 200 is ok 
    assert response.status_code == 200

# test login page 
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


# test user info without a signed in account 
def test_user_info(client):
    # loads user html
    response= client.get('/user_info')
    # html code 302 should appear as no account is signed in (redirect to login)
    assert response.status_code == 302
    assert response.headers['Location'] == '/Login' 

# test user info while signed in 
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

    # reads if user id is 2 from form
    assert b"<strong>User ID:</strong> 2" in response.data



    








