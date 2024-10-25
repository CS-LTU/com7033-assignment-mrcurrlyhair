import sqlite3
import csv 


# File paths 
db_path = 'Database.db'
csv_path = 'healthcare-dataset-stroke-data.csv'


con = sqlite3.connect(db_path)
cur = con.cursor()

#Creating the table for patient infoimation 
cur.execute('''
    CREATE TABLE IF NOT EXISTS patient(
        id INTEGER PRIMARY KEY, 
        gender TEXT(6) NOT NULL, 
        age FLOAT NOT NULL, 
        hypertension BOOLEAN NOT NULL, 
        heart_disease BOOLEAN NOT NULL, 
        ever_married TEXT(3) NOT NULL, 
        work_type TEXT NOT NULL, 
        residence_type TEXT NOT NULL, 
        avg_glucose_level FLOAT NOT NULL, 
        bmi FLOAT, 
        smoking_status TEXT NOT NULL, 
        stroke BOOLEAN NOT NULL,
        user_id AUTO_INCREMENT INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(id)
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
   
    
# testing opening csv 
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
 
# inserting data test 
    for i,row in enumerate(csv_reader):
        cur.execute('''
            SELECT COUNT(*) FROM patient WHERE id = ?
        ''', (row[0],))
        
        if cur.fetchone()[0] == 0:
            cur.execute('''
                INSERT INTO patient (
                    id, gender, age, hypertension, heart_disease, ever_married,
                    work_type, residence_type, avg_glucose_level, bmi,
                    smoking_status, stroke, user_id
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                i+1
            ))


# Implementing user_id


# upload changes
con.commit()

# close connection 
con.close()



