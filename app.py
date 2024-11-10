from flask import Flask, request, jsonify, render_template, session, redirect, url_for, abort, request, flash, get_flashed_messages  
import pymongo
import sqlite3
import hashlib
import re 

app = Flask(__name__, static_folder='static')
app.secret_key = 'assignment database'

# Mongo connection
mdb_path = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mdb_path)
db = client["medicalDB"]
user_collection = db["user"]

# SQLite connection
sqlite_db_path = "Database.db"
def get_sqlite_connection():
    return sqlite3.connect(sqlite_db_path)

# Hashing password
def hashing_pass(text):
    text = text.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(text)
    return hash.hexdigest()


# Home page
@app.route('/')
def landing():
    print('test landing page')
    return render_template('Home.html')

# Information page
@app.route('/Information')
def information():
    print('test information')
    return render_template("Information.html")

# Get user info page
@app.route('/user_info')
def user_info():
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']

    # Fetch patient from MongoDB
    user = user_collection.find_one({"u_id": user_id})

    # Fetch patient from sql
    con = get_sqlite_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM patient WHERE p_id = ?", (user_id,))
    patient_info = cur.fetchone()
    con.close()

    if user and patient_info:
        return render_template("UserInfo.html", user=user, patient=patient_info)
    else:
        default_user = {
            "u_id": user_id,
            "u_username": user.get("u_username", "N/A") if user else "N/A"
        }
        default_patient = (
            patient_info if patient_info else ("N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")
        )

        return render_template("UserInfo.html", user=default_user, patient=default_patient)

# Update health info
@app.route('/update_info', methods=['GET', 'POST'])
def update_info():
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']

    if request.method == 'POST':
        # Get updated information from form
        p_gender = request.form['p_gender']
        p_age = request.form['p_age']
        p_hypertension = request.form['p_hypertension']
        p_heart_disease = request.form['p_heart_disease']
        p_ever_married = request.form['p_ever_married']
        p_work_type = request.form['p_work_type']
        p_residence_type = request.form['p_residence_type']
        p_avg_glucose_level = request.form['p_avg_glucose_level']
        p_bmi = request.form['p_bmi']
        p_smoking_status = request.form['p_smoking_status']
        p_stroke = request.form['p_stroke']
        

        # Update the patient record 
        con = get_sqlite_connection()
        cur = con.cursor()
        cur.execute("""
            UPDATE patient
            SET p_gender = ?, p_age = ?, p_hypertension = ?, p_heart_disease = ?, 
                p_ever_married = ?, p_work_type = ?, p_residence_type = ?, 
                p_avg_glucose_level = ?, p_bmi = ?, p_smoking_status = ?, p_stroke = ?
            WHERE p_id = ?
        """, (p_gender, p_age, p_hypertension, p_heart_disease, p_ever_married, p_work_type, 
              p_residence_type, p_avg_glucose_level, p_bmi, p_smoking_status, p_stroke, user_id))
        con.commit()
        con.close()

        return redirect(url_for('user_info'))

    # Get current patient info
    con = get_sqlite_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM patient WHERE p_id = ?", (user_id,))
    patient_info = cur.fetchone()
    con.close()

    # Update the current patient info to the template
    return render_template('UpdateInfo.html', patient=patient_info)


# Sign up page
@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        hashed_password = hashing_pass(password)
        password_requirements = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    

        # Does both passwords match 
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('Signup'))
        
        # Check password requirements
        if not re.match(password_requirements, password):
            flash("Password must be at least 8 characters, include an uppercase letter, a lowercase letter, a number, and a special character.")
            return redirect(url_for('Signup'))

        # Highest p_id +1 in sql p_id
        con = get_sqlite_connection()
        cur = con.cursor()
        cur.execute("SELECT MAX(p_id) FROM patient")
        max_p_id = cur.fetchone()[0]
        new_p_id = max_p_id + 1 if max_p_id is not None else 1
        con.close()

        # Does user already exist?
        if user_collection.find_one({"u_username": username}):
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for('Signup'))

        # Insert user Mongo
        user_collection.insert_one({
            "u_id": new_p_id, 
            "u_username": username, 
            "u_password": hashed_password,
            "is_admin": False })
        
        # Create user in SQLite
        con = get_sqlite_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO patient (p_id, p_gender, p_age, p_hypertension, p_heart_disease, p_ever_married, p_work_type, p_residence_type, p_avg_glucose_level, p_bmi, p_smoking_status, p_stroke) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (new_p_id, 'Unknown', 0, 0, 0, 'No', 'Unknown', 'Unknown', 0.0, 0.0, 'Unknown', 0))
        con.commit()
        con.close()

        flash("Account created successfully. Please log in.")
        return redirect(url_for('Login'))
    
    return render_template('Signup.html')


# Login page
@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # find patient in mongo 
        user = user_collection.find_one({"u_username": username})

        # hashing password
        hashed_input_password = hashing_pass(password)

        # does user exist and has a matching password
        if user and user['u_password'] == hashed_input_password:
            session['user_id'] = user['u_id']
            session['is_admin'] = user.get('is_admin', False)  

            if session['is_admin']:
                return redirect(url_for('admin'))  
            else:
                return redirect(url_for('user_info'))  
        else:
            # error splash screen 
            flash("Wrong username/password. Please try again.")
            return redirect(url_for('Login'))

    return render_template('Login.html')


# Logout page
@app.route('/logout')
def logout():
    session.clear()  # clear all session data
    flash("Successfully logged out ")
    return redirect(url_for('Login'))  # redirect to home page

# Admin route
@app.route('/admin', methods=['GET'])
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('Login'))
    
    # Fetch users from MongoDB
    users = list(user_collection.find({}, {"_id": 0, "u_id": 1, "u_username": 1}))
    
    # Fetch patients from SQLite
    con = get_sqlite_connection()
    cur = con.cursor()
    cur.execute("SELECT p_id, p_gender, p_age FROM patient")
    patients = cur.fetchall()
    con.close()
    
    return render_template('Admin.html', users=users, patients=patients)

# Delete account route for patient 
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']
    is_admin = session.get('is_admin', False)

    # Delete from mongo
    user_collection.delete_one({"u_id": user_id})

    # Delete from sql
    con = get_sqlite_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM patient WHERE p_id = ?", (user_id,))
    con.commit()
    con.close()

    # Clear session 
    session.clear()
    flash("Account deleted successfully.")
    if is_admin:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('Login'))

# Delete account route for admin 
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('Login'))

    # Delete user from mongo
    user_collection.delete_one({"u_id": user_id})

    # Delete patient from sql
    con = get_sqlite_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM patient WHERE p_id = ?", (user_id,))
    con.commit()
    con.close()

    flash("User deleted successfully.")
    return redirect(url_for('admin'))




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
