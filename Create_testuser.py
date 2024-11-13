from app import user_collection
from Mongo_Loader import hashing_pass

# MongoDB setup to create a test user
def create_testuser():

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
