import sqlite3
import csv 
import random
import string 

# File paths 
db_path = 'Database.db'
csv_path = 'healthcare-dataset-stroke-data.csv'


con = sqlite3.connect(db_path)
cur = con.cursor()

#Creating the table for patient infoimation 
cur.execute('''
    CREATE TABLE IF NOT EXISTS patient(
        p_id INTEGER PRIMARY KEY, 
        p_gender TEXT(6) NOT NULL, 
        p_age FLOAT NOT NULL, 
        p_hypertension BOOLEAN NOT NULL, 
        p_heart_disease BOOLEAN NOT NULL, 
        p_ever_married TEXT(3) NOT NULL, 
        p_work_type TEXT NOT NULL, 
        p_residence_type TEXT NOT NULL, 
        p_avg_glucose_level FLOAT NOT NULL, 
        p_bmi FLOAT, 
        p_smoking_status TEXT NOT NULL, 
        p_stroke BOOLEAN NOT NULL    
    )
''')

#Creating the table for patient login
cur.execute('''
    CREATE TABLE IF NOT EXISTS user(
        u_id INTEGER PRIMARY KEY AUTOINCREMENT,
        u_username TEXT(16),
        u_password TEXT(16)
    )
''')


# String to integer / yes and no (may not use)
def yes_to_one(yesno):
    if yesno.lower() == 'yes':
        return True
    else:
        return False
    
# cleaning bmi data 
def bmi_cleaning(value):
    if value.strip() == '' or value.lower == 'n/a':
        return None
    
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


# testing opening csv 
with open(csv_path) as csv_file:
    table = csv.reader(csv_file)
    next(table)

 
# inserting data test 
    for row in table:
        cur.execute('''
            SELECT COUNT(*) FROM patient WHERE p_id = ?
        ''', (row[0],))
        
        if cur.fetchone()[0] == 0:
            cur.execute('''
                INSERT INTO patient (
                    p_id, p_gender, p_age, p_hypertension, p_heart_disease, p_ever_married,
                    p_work_type, p_residence_type, p_avg_glucose_level, p_bmi,
                    p_smoking_status, p_stroke
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(row[0]),            # id
                row[1],                 # gender
                float(row[2]),          # age
                bool(int(row[3])),      # hypertension
                bool(int(row[4])),      # heart_disease
                row[5],                 # ever_married
                row[6],                 # work_type
                row[7],                 # residence_type
                float(row[8]),          # avg_glucose_level
                bmi_cleaning(row[9]),   # bmi
                row[10],                # smoking_status
                bool(int(row[11])),     # stroke
            ))


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

#close the file 
csv_file.close()

# upload changes
con.commit()

# close connection 
con.close()
  