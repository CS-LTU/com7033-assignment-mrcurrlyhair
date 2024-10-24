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
        id INTEGER PRIMART KEY, 
        gender TEXT(6), 
        age INTEGER, 
        hypertension , 
        heart_disease, 
        ever_married, 
        work_type, 
        residence_type, 
        avg_glucose_level, 
        bmi, 
        smoking_status, 
        stroke
    )
''')
        

