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
        p_id INTEGER PRIMARY KEY, 
        p_gender TEXT(6) NOT NULL, 
        p_age INTEGER NOT NULL, 
        p_hypertension BOOLEAN NOT NULL, 
        p_heart_disease BOOLEAN NOT NULL, 
        p_ever_married BOOLEAN NOT NULL, 
        p_work_type TEXT NOT NULL, 
        p_residence_type TEXT NOT NULL, 
        p_avg_glucose_level FLOAT NOT NULL, 
        p_bmi FLOAT, 
        p_smoking_status BOOLEAN NOT NULL, 
        p_stroke BOOLEAN NOT NULL
    )
''')



