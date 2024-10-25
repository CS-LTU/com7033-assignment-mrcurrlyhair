import sqlite3
import csv 




# File paths 
db_path = 'Database.db'

con = sqlite3.connect(db_path)
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




