import pymongo
import hashlib
from app import app, get_sqlite_connection
from Mongo_Loader import hashing_pass
from Create_Admin import user_collection

# Admin details
test_username = "testuser"
test_password = "Churchill!2" 
hashed_password = hashing_pass(test_password)

# Creating admin 
admin_user = {
    "u_id": 2, # Ensuring this u_id is unique as no one else occupies 2
    "u_username": test_username,
    "u_password": hashed_password,
    "is_admin": True
}

# Adding test user to mongo , if already exists prints admin is already created 
try:
    user_collection.insert_one(admin_user)
    print("testuser created")
except pymongo.errors.DuplicateKeyError:
    print("Already created testuser")