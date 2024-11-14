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

    # Creating Testuser dictionrary 
    test_user = {
        "u_id": 2,  # no user uses u_id of 2 , unique to testuser 
        "u_username": test_username,
        "u_password": hashed_password,
        "is_admin": False
    }

    # Adding testuser to Mogno
    user_collection.insert_one(test_user)
    print("Testuser created in Mongo")

def delete_testuser_mongo():
    # Removes the testuser with a specific u_id in Mongo
    user_collection.delete_one({"u_id": 2})
    print("Testuser deleted in Mongo")

# Connect to SQL
sqlite_db_path = 'Database.db'
con = sqlite3.connect(sqlite_db_path)
cur = con.cursor()

def create_testuser_sql(cur):
    # Insert testuser into SQL with p_id of 2
    cur.execute('''
        INSERT INTO patient (
            p_id, p_gender, p_age, p_hypertension, p_heart_disease, p_ever_married,
            p_work_type, p_residence_type, p_avg_glucose_level, p_bmi,
            p_smoking_status, p_stroke
        ) 
        VALUES (?, ?, 0, 0, 0, 'No', 'Unknown', 'Unknown', 0.0, 0.0, 'Unknown', 0) 
    ''', (2, 'test'))
    print("Test user created in SQL")

def delete_testuser_sql(cur):
    # Removes the testuser with a specific p_id in SQL
    cur.execute("DELETE FROM patient WHERE p_id = ?", (2,))
    print("Testuser deleted in SQL")


# fixture that runs start_and_delete_Testuser once.
@pytest.fixture(scope="session", autouse=True)

def start_and_delete_Testuser():
    # Connect to SQL
    con = get_sqlite_connection()
    cur = con.cursor()

    try:
        # Create test user in MongoDB and SQLite
        create_testuser_mongo()
        create_testuser_sql(cur)
        con.commit()  # Commit changes in SQL

        # Allows tests to run then after they have , returns here where it deletes the testuser account 
        yield

    finally:
        # Delete test user in Mongo and SQL
        delete_testuser_mongo()
        delete_testuser_sql(cur)
        con.commit()  # Save deletions in SQ
        con.close()   # Close SQL connection


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

    # Reads if user id is 2 in the form (Mongo test)
    assert b"<strong>User ID:</strong> 2" in response.data

    # Reads if gender is test in the form (SQL test)
    assert b"<strong>Gender:</strong> test" in response.data


    








