import sqlite3
import csv 
import random
import string 

# File paths 
sqlite_db_path = 'Database.db'
csv_path = 'healthcare-dataset-stroke-data.csv'


con = sqlite3.connect(sqlite_db_path)
cur = con.cursor()

# Creating the table for patient infoimation 
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
    
# Cleaning bmi data 
def bmi_cleaning(value):
    if value.strip() == '' or value.lower == 'n/a':
        return None
    
# Testing opening csv 
with open(csv_path) as csv_file:
    table = csv.reader(csv_file)
    next(table)

 
# Inserting data test 
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

# Close the file 
csv_file.close()

# Upload changes
con.commit()

# Close connection 
con.close()
  