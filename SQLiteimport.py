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

# nts testing opening csv 
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

#nts inserting data test 
    for row in csv_reader:
        cur.execute('''
                    SELECT COUNT (*) FROM patient WHERE p_id = ? 
                    ''', (row[0]))
        if cur.fetchone()[0] == 0:
            cur.execute('''
                        INSERT INTO patient (p_id) 
                        VALUES(?)
                        ''', (row[0]) )
                    




# upload changes
con.commit()

# close connection 
con.close()



