from flask import Flask, request, jsonify, render_template, session, redirect, url_for, abort 
import pymongo
import sqlite3
import hashlib

# need to add comment
app = Flask(__name__, static_folder='static')
app.secret_key = 'assignmentdatabase'

# MongoDB setup
mdb_path = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mdb_path)
db = client["medicalDB"]
user_collection = db["user"]

# SQLite setup
sqlite_db_path = "Database.db"

def get_sqlite_connection():
    return sqlite3.connect(sqlite_db_path)

# hashing password
def hashing_pass(text):
    text = text.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(text)
    return hash.hexdigest()


# get user info page
@app.route('/user_info')
def user_info():
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']
    user = user_collection.find_one({"u_id": user_id})
    if user:
        return render_template("UserInfo.html", user=user)
    else:
        return "User not found."



# delete a user
@app.route('/delete_user/<p_id>', methods=['DELETE'])
def delete_user(p_id):
    result = user_collection.delete_one({"u_id": p_id})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted successfully."})
    else:
        return jsonify({"message": "User not found."})

# # read all patient records from SQLite
# @app.route('/get_patients', methods=['GET'])
# def get_patients():
#     con = get_sqlite_connection()
#     cur = con.cursor()
#     cur.execute("SELECT * FROM patient")
#     patients = cur.fetchall()
#     con.close()
    
#     patient_list = [
#         {
#             "p_id": patient[0],
#             "p_gender": patient[1],
#             "p_age": patient[2],
#             "p_hypertension": patient[3],
#             "p_heart_disease": patient[4],
#             "p_ever_married": patient[5],
#             "p_work_type": patient[6],
#             "p_residence_type": patient[7],
#             "p_avg_glucose_level": patient[8],
#             "p_bmi": patient[9],
#             "p_smoking_status": patient[10],
#             "p_stroke": patient[11]
#         } for patient in patients
#     ]
    
    # return jsonify(patient_list)

# home page
@app.route('/')
def landing():
    print('test landing page')
    return render_template('Home.html')

# info page
@app.route('/Information')
def information():
    print('test information')
    return render_template("Information.html")

# sign up page
@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashing_pass(password)

        # maximum +1 in sql p_id
        con = get_sqlite_connection()
        cur = con.cursor()
        cur.execute("SELECT MAX(p_id) FROM patient")
        max_p_id = cur.fetchone()[0]
        new_p_id = max_p_id + 1 if max_p_id is not None else 1
        con.close()

        # does user exist?
        if user_collection.find_one({"u_username": username}):
            return "User already exists. Please try again."

        # insert user mongo
        user_collection.insert_one({"u_id": new_p_id, "u_username": username, "u_password": hashed_password})
        
        #create user sql
        con = get_sqlite_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO patient (p_id, p_gender, p_age, p_hypertension, p_heart_disease, p_ever_married, p_work_type, p_residence_type, p_avg_glucose_level, p_bmi, p_smoking_status, p_stroke) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (new_p_id, 'Unknown', 0, 0, 0, 'No', 'Unknown', 'Unknown', 0.0, 0.0, 'Unknown', 0))
        con.commit()
        con.close()

        return redirect(url_for('Login'))
    
    return render_template('Signup.html')


# login page
@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashing_pass(password)

        # does user/pass match
        user = user_collection.find_one({"u_username": username, "u_password": hashed_password})
        if user:
            session['user_id'] = user['u_id']
            return redirect(url_for('user_info'))
        else:
            return "Invalid username or password. Please try again."

    print('test Login page')
    return render_template("Login.html")

# logout page
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('landing'))  # Redirect to home page

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
