# Import the required library
from pymongo import MongoClient
import sqlite3
import random
import string

# Establish a connection to the MongoDB server
# Replace '<your_connection_string>' with your actual MongoDB URI
client = MongoClient('<your_connection_string>')

# Create or connect to a database
# If the database doesn't exist, MongoDB will create it for you when you add data
db = client['my_database']

# Create or connect to a collection within the database
users_collection = db['users']

# Word list for generating usernames
word_list = [
    'apple', 'banana', 'cherry', 'dragon', 'eagle', 'falcon', 'grape', 'honey', 'island', 'jungle',
    'kiwi', 'lemon', 'mango', 'night', 'orange', 'peach', 'queen', 'river', 'stone', 'tiger',
    'amber', 'breeze', 'crystal', 'dawn', 'ember', 'forest', 'galaxy', 'hazel', 'ivy', 'jade',
    'kelp', 'lotus', 'mist', 'nebula', 'oasis', 'pearl', 'quartz', 'rose', 'shadow', 'thunder',
    'unity', 'violet', 'whisper', 'yonder', 'zenith', 'aurora', 'blizzard', 'cascade', 'delight', 
    'echo', 'frost', 'glow', 'harbor', 'infinity', 'jasmine', 'kestrel', 'lilac', 'meadow', 
    'nebula', 'ocean', 'petal', 'quiver', 'raven', 'sky', 'twilight', 'uplift', 'voyage', 
    'wild', 'zen', 'autumn', 'birch', 'canyon', 'daisy', 'ever', 'fern', 'glacier', 'horizon', 
    'iris', 'jewel', 'knight', 'lunar', 'mystic', 'nova', 'opal', 'prairie', 'quail', 'ripple', 
    'sparrow', 'trek', 'umbra', 'vortex', 'willow', 'yarrow', 'zephyr', 'brave', 'clover', 
    'dandelion', 'fable', 'grace', 'haven', 'ignite', 'journey', 'kindle', 'legend', 'mirth', 
    'nectar', 'oracle', 'pioneer', 'quest', 'radiant', 'serene', 'tempest', 'unity', 'valor', 
    'wander', 'xenon', 'yule'
]

# Generating random username for existing users
def gen_username(length=18):
    word1 = random.choice(word_list)
    word2 = random.choice(word_list)
    return word1.capitalize() + word2.capitalize()

# Generating random password for existing users
def gen_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

# Connect to the SQLite database
con = sqlite3.connect('database.db')
cur = con.cursor()

# Get patient data from the patients table
cur.execute('SELECT p_id FROM patients')
patients = cur.fetchall()

# Inputting usernames, passwords, and foreign keys generated
for patient in patients:
    p_id = patient[0]
    username = gen_username()
    password = gen_password()
    users_collection.insert_one({
        "u_username": username,
        "u_password": password,
        "p_id": p_id
    })

# Close the SQLite connection
con.close()

# Close the MongoDB connection
client.close()
