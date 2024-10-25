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

# String to integer / yes and no (may not use)
def yes_to_one(yesno):
    if yesno.lower() == 'yes':
        return 1
    else:
        return 0

# cleaning bmi data 
def bmi_cleaning(value):
    if value.strip() == '' or value.lower == 'n/a':
        return None
   
    
# testing opening csv 
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
 
# inserting data test 
    for row in csv_reader:
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
                int(row[0]),            # p_id
                row[1],                 # p_gender
                float(row[2]),          # p_age
                bool(int(row[3])),      # p_hypertension
                bool(int(row[4])),      # p_heart_disease
                row[5],                 # p_ever_married
                row[6],                 # p_work_type
                row[7],                 # p_residence_type
                float(row[8]),          # p_avg_glucose_level
                bmi_cleaning(row[9]),   # p_bmi
                row[10],                # p_smoking_status
                bool(int(row[11]))      # p_stroke
            ))


# upload changes
con.commit()

# close connection 
con.close()



