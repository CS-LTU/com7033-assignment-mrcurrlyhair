import pytest
import pymongo
import sqlite3
from Mongo_Loader import hashing_pass


# Connect to Mongo
client = MongoClient("mongodb://localhost:27017/")
db = client["medicalDB"]
user_collection = db["user"]

#Connect to SQLite 
sqlite_db_path = "Database.db"
def get_sqlite_connection():
    return sqlite3.connect(sqlite_db_path)

