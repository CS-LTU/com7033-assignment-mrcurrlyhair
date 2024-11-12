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

