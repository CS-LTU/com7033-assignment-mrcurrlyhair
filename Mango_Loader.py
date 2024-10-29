import sqlite3
import csv 
import random
import string 


# File paths 
mdb_path = 'mDatabase.db'
csv_path = 'healthcare-dataset-stroke-data.csv'


con = sqlite3.connect(mdb_path)
cur = con.cursor()



#Creating the table for patient login
cur.execute('''
    CREATE TABLE IF NOT EXISTS user(
        u_id INTEGER PRIMARY KEY AUTOINCREMENT,
        u_username TEXT(16),
        u_password TEXT(16)
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
def gen_username(lenght =18):
    word1 = random.choice(word_list)
    word2 = random.choice(word_list)
    return word1.capitalize() + word2.capitalize()

# generating random password for existing users 
def gen_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))


# getting the amount of rows from pateint  
cur.execute('SELECT COUNT(*) FROM patient')
patient_count = cur.fetchone()[0]


#inputting username and passwords generated 
for i in range(patient_count): 
    username = gen_username()
    password = gen_password()
    cur.execute('''
        INSERT INTO user (u_username, u_password)
        VALUES (?, ?)
    ''', (username, password))


# upload changes
con.commit()

# close connection 
con.close()
