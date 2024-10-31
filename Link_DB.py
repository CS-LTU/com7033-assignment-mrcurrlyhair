import sqlite3
from pymongo import MongoClient

# Connect to SQLite database
sqlite_conn = sqlite3.connect('patient_records.db')
sqlite_cursor = sqlite_conn.cursor()

# Connect to MongoDB database
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['user_database']
mongo_collection = mongo_db['user_credentials']

# Example function to link patient data using p_id as a primary key
def link_patient_data():
    # Fetch patient data from SQLite
    sqlite_cursor.execute("SELECT p_id, name, age, bmi FROM patients")
    patients = sqlite_cursor.fetchall()
    
    for patient in patients:
        p_id = patient[0]
        
        # Fetch corresponding user credentials from MongoDB using p_id
        user = mongo_collection.find_one({"user_id": p_id})
        
        if user:
            print(f"Linked Data for Patient ID {p_id}: Name: {patient[1]}, Age: {patient[2]}, BMI: {patient[3]}")
        else:
            print(f"No user data found for Patient ID {p_id}")

# Link patient data using p_id as a primary key
link_patient_data()

# Close connections
sqlite_conn.close()
mongo_client.close()
