import sqlite3
import csv 
import random
import string 




# File paths 
db_path = 'Database.db'

con = sqlite3.connect(db_path)
con.execute('PRAGMA foreign_keys = ON;')
cur = con.cursor()

#Creating the table for patient infoimation 
cur.execute('''
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        username TEXT(16),
        password TEXT(16),
        patient_id INTEGER,
        FOREIGN KEY(patient_id) REFERENCES patient(id)
    )
''')

#for username
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


# generating random username for existing users 
def gen_username(lenght=18):
    word1 = random.choice(word_list)
    word2 = random.choice(word_list)
    return word1.capitalize() + word2.capitalize()

# generating random password for existing users 
def gen_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))


# adding the random username and passwords into the database/user table
for _ in range(5111):  
    username = gen_username()
    password = gen_password()
    cur.execute('''
        INSERT INTO user (username, password, patient_id)
        VALUES (?, ?, NULL)
    ''', (username, password))

# upload changes
con.commit()

# close connection 
con.close()


