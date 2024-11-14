import pymongo
import hashlib
import sqlite3
from app import app
from Mongo_Loader import hashing_pass 


# Mongo connection
mdb_path = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mdb_path)
db = client["medicalDB"]
user_collection = db["user"]

# SQLite connection
sqlite_db_path = 'Database.db'
con = sqlite3.connect(sqlite_db_path)
cur = con.cursor()

# Admin details
admin_username = "admin"
admin_password = "Churchill!1" # Hashing admin password
hashed_password = hashing_pass(admin_password)

# Creating admin in Mongo
admin_mongo= {
    "u_id": 1, # no user uses id of 1 , unique to admin 
    "u_username": admin_username,
    "u_password": hashed_password,
    "is_admin": True
}

# Adding admin to mongo , if already exists prints already created admin
try:
    user_collection.insert_one(admin_mongo)
    print("Admin created in Mongo")
except pymongo.errors.DuplicateKeyError:
    print("Already created admin in Mongo")


cur.execute('SELECT COUNT(*) FROM patient WHERE p_id = ?', (1,))
if cur.fetchone()[0] == 0:
    cur.execute('''
        INSERT INTO patient (
            p_id, p_gender, p_age, p_hypertension, p_heart_disease, p_ever_married,
            p_work_type, p_residence_type, p_avg_glucose_level, p_bmi,
            p_smoking_status, p_stroke
        ) 
        VALUES (?,'Unknown', 0, 0, 0, 'No', 'Unknown', 'Unknown', 0.0, 0.0, 'Unknown', 0)
    ''', (1,))
    print("Admin created in SQL")
else:
    print("Already created admin in SQL")

# Commit changes and close the SQLite connection
con.commit()
con.close()