import pymongo
import hashlib
from app import app, get_sqlite_connection
from Mongo_Loader import hashing_pass


# Mongo connection
mdb_path = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mdb_path)
db = client["medicalDB"]
user_collection = db["user"]

# Admin details
admin_username = "admin"
admin_password = "Churchill!1" # Hashing admin password, more important than user passwords
hashed_password = hashing_pass(admin_password)

# Creating admin 
admin_user = {
    "u_id": 1, # Ensuring this u_id is unique as no one else occupies 1 
    "u_username": admin_username,
    "u_password": hashed_password,
    "is_admin": True
}

# Adding admin to mongo , if already exists prints admin is already created 
try:
    user_collection.insert_one(admin_user)
    print("Admin created")
except pymongo.errors.DuplicateKeyError:
    print("Already created admin")