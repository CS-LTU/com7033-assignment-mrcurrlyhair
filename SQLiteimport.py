import sqlite3
import csv 

# File paths 
db_path = 'Database.db'
csv_path = 'healthcare-dataset-stroke-data.csv'





con = sqlite3.connect("Database.db")

cur = con.cursor()

cur.execute("CREATE TABLE Patient(id, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke)")

