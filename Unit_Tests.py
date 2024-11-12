import unittest
from flask import get_flashed_messages
from app import app, user_collection, client, db, hashing_pass
from pymongo import MongoClient
import sqlite3

# Connect to Mongo
client = MongoClient("mongodb://localhost:27017/")
db = client["medicalDB"]
user_collection = db["user"]

#Connect to SQLite 
sqlite_db_path = "Database.db"
def get_sqlite_connection():
    return sqlite3.connect(sqlite_db_path)

class TestFlaskRoutes(unittest.TestCase):
    # Creates a test 'enviroment'
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'  
        self.client = app.test_client()
        
        user_collection.delete_many({"u_username": "testuser"})
        con = get_sqlite_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM patient WHERE p_id = ?", (2,))
        con.commit()
        con.close()

    # Deletes the test 'enviroment' data
    def tearDown(self):
        # Clean up test data after each test
        user_collection.delete_many({"u_username": "testuser"})
        con = get_sqlite_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM patient WHERE p_id = ?", (2,))
        con.commit()
        con.close()

    # Test Singup
    def test_signup(self):
        response = self.client.post('/Signup', data={
            'username': 'testuser',
            'password': 'Testpass!123', # Has to meet password requirements 
            'confirm_password': 'Testpass!123'
        }, follow_redirects=True)
        
        # Check for a redirect to the login page after successful signup
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/Login', response.data)  # Check redirect happened to /Login
        
        self.assertIn(b"Account created successfully. Please log in.", response.data)

    def test_login(self):
        # Insert test user for login test
        user_collection.insert_one({
            "u_id": 2, 
            "u_username": "testuser", 
            "u_password": hashing_pass("Testpass!123"),
            "is_admin": False 
        })

        response = self.client.post('/Login', data={
            'username': 'testuser',
            'password': 'Testpass!123'
        }, follow_redirects=True)

        # Check that the login was successful and user was redirected to user_info
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/user_info', response.data)  # Confirm redirect to /user_info

        # Clean up
        user_collection.delete_one({"u_username": "testuser"})

    # For when someone isnt signed in.    
    def test_access_control_user_info(self):
        response = self.client.get('/user_info')
        self.assertEqual(response.status_code, 302)  # Should redirect to login if not logged in

    def test_update_info(self):
        # Log in user
        with self.client.session_transaction() as session:
            session['user_id'] = 2

        response = self.client.post('/update_info', data={
            'p_gender': 'Male',
            'p_age': 21,
            'p_hypertension': 0,
            'p_heart_disease': 0,
            'p_ever_married': 'No',
            'p_work_type': 'Private',
            'p_residence_type': 'Urban',
            'p_avg_glucose_level': 80.0,
            'p_bmi': 22.5,
            'p_smoking_status': 'Smokes',
            'p_stroke': 0
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after updating info

    def test_logout(self):
        # Log in as test user (p/u_id = 2)
        with self.client.session_transaction() as session:
            session['user_id'] = 2

        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  # Should redirect after logout

    def test_delete_account(self):
        # Insert test user into mongo
        user_collection.insert_one({
            "u_id": 2, 
            "u_username": "testuser", 
            "u_password": hashing_pass("Testpass!123"),
            "is_admin": False 
        })
        # Insert test user into SQLite
        con = get_sqlite_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO patient (p_id, p_gender, p_age, p_hypertension, p_heart_disease, p_ever_married, p_work_type, p_residence_type, p_avg_glucose_level, p_bmi, p_smoking_status, p_stroke) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (2, 'Unknown', 0, 0, 0, 'No', 'Unknown', 'Unknown', 0.0, 0.0, 'Unknown', 0))
        con.commit()
        con.close()

        # Log in user
        with self.client.session_transaction() as session:
            session['user_id'] = 2

        # Deletes the test user 
        response = self.client.post('/delete_account')
        self.assertEqual(response.status_code, 302)  # Should redirect after account deletion
        self.assertNotIn(b'testuser', user_collection.find({}).distinct("u_username"))


class TestHashingPass(unittest.TestCase):

# Testing if different passwords have different hashes
    def test_hashing_pass_diff_input(self):
        input_text1 = "Test_password"
        input_text2 = "Password_test"
        hash1 = hashing_pass(input_text1)
        hash2 = hashing_pass(input_text2)
        self.assertNotEqual(hash1, hash2, "Different inputs , should be different hashes")


# Testing length of the hash, SHA256 should equal 64 characters
    def test_hashing_pass_length(self):
        input_text = "Test_password"
        hashed_output = hashing_pass(input_text)
        self.assertEqual(len(hashed_output), 64, "Hash length is incorrect.")

if __name__ == '__main__':
    unittest.main()
