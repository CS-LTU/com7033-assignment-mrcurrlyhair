import pymongo
import sqlite3
import csv
import random
import string

# File paths 
mdb_path = "mongodb://localhost:27017/"
sqlite_db_path = "Database.db"
csv_path = "healthcare-dataset-stroke-data.csv"

# Connect to MongoDB
client = pymongo.MongoClient(mdb_path)
db = client["medicalDB"]
user_collection = db["user"]

# Connect to SQLite
sqlite_con = sqlite3.connect(sqlite_db_path)
sqlite_cur = sqlite_con.cursor()

# for username
word_list = [
    "apple", "banana", "cherry", "dragon", "eagle", "falcon", "grape", "honey", "island", "jungle",
    "kiwi", "lemon", "mango", "night", "orange", "peach", "queen", "river", "stone", "tiger",
    "amber", "breeze", "crystal", "dawn", "ember", "forest", "galaxy", "hazel", "ivy", "jade",
    "kelp", "lotus", "mist", "nebula", "oasis", "pearl", "quartz", "rose", "shadow", "thunder",
    "unity", "violet", "whisper", "yonder", "zenith", "aurora", "blizzard", "cascade", "delight", 
    "echo", "frost", "glow", "harbor", "infinity", "jasmine", "kestrel", "lilac", "meadow", 
    "nebula", "ocean", "petal", "quiver", "raven", "sky", "twilight", "uplift", "voyage", 
    "wild", "zen", "autumn", "birch", "canyon", "daisy", "ever", "fern", "glacier", "horizon", 
    "iris", "jewel", "knight", "lunar", "mystic", "nova", "opal", "prairie", "quail", "ripple", 
    "sparrow", "trek", "umbra", "vortex", "willow", "yarrow", "zephyr", "brave", "clover", 
    "dandelion", "fable", "grace", "haven", "ignite", "journey", "kindle", "legend", "mirth", 
    "nectar", "oracle", "pioneer", "quest", "radiant", "serene", "tempest", "unity", "valor", 
    "wander", "xenon", "yule"
]

# generating random username for existing users 
def gen_username(lenght=18):
    word1 = random.choice(word_list)
    word2 = random.choice(word_list)
    return word1.capitalize() + word2.capitalize()

# generating random password for existing users 
def gen_password(length=8):
    return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

# Getting the number of patients from the SQLite patient table
sqlite_cur.execute("SELECT COUNT(*) FROM patient")
patient_count = sqlite_cur.fetchone()[0]

# Inserting username, passwords, and user ID generated for each patient
user_records = []
for i in range(patient_count):
    user_id = i + 1
    username = gen_username()
    password = gen_password()
    user_records.append({"u_id": user_id, "u_username": username, "u_password": password})

if user_records:
    user_collection.insert_many(user_records)

# Close connections
sqlite_con.close()
client.close()
