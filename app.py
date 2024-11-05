from flask import Flask, request, jsonify, render_template, session, redirect, url_for, abort 
import pymongo
import sqlite3
import hashlib

# need to add comment
app = Flask(__name__, static_folder='static')
app.secret_key = 'assignmentdatabase'

# mongo connection
mdb_path = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mdb_path)
db = client["medicalDB"]
user_collection = db["user"]

# sqlite connection
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

#update health info
@app.route('/update_info', methods=['GET', 'POST'])
def update_info():
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashing_pass(password)

        # Update user info in MongoDB
        user_collection.update_one({"u_id": user_id}, {"$set": {"u_username": username, "u_password": hashed_password}})
        return redirect(url_for('user_info'))

    user = user_collection.find_one({"u_id": user_id})
    return render_template('UpdateInfo.html', user=user)


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
            return redirect(url_for('Signupfail'))

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

# sign up fail page
@app.route('/Signupfail', methods=['GET', 'POST'])
def Signupfail():
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
            return redirect(url_for('Signupfail'))

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
    
    return render_template('Signupfail.html')


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
            return redirect(url_for('Login_fail'))

    print('test Login page')
    return render_template("Login.html")

# login faliure page
@app.route('/Loginfail', methods=['GET', 'POST'])
def Login_fail():
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
            return redirect(url_for('Login_fail'))
    print('test Login page')
    return render_template("LoginFail.html")



# logout page
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('landing'))  # Redirect to home page

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
