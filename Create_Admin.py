import pymongo
import hashlib

# MongoDB connection
mdb_path = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mdb_path)
db = client["medicalDB"]
user_collection = db["user"]

# hashing password
def hashing_pass(text):
    text = text.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(text)
    return hash.hexdigest()


#admin details
admin_username = "admin"
admin_password = "12345678" 
hashed_password = hashing_pass(admin_password)

#creating admin 
admin_user = {
    "u_id": 1,  # Ensure this ID is unique
    "u_username": admin_username,
    "u_password": hashed_password,
    "is_admin": True
}
#
try:
    user_collection.insert_one(admin_user)
    print("Admin created")
except pymongo.errors.DuplicateKeyError:
    print("Already requested")