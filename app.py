from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#importing database 
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'Database.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = FALSE 
db = SQLAlchemy(app)


#Landing page
@app.route('/')
def landing():
    print('test landing page')
    return render_template('Home.html')

#Infomation page
@app.route('/Information')
def infomation():
    print('test information')
    return render_template("Information.html")

#Sign up page 
@app.route('/Signup', methods=['GET', 'POST'])
def Signup():



    print('test sing up page')
    return render_template('Signup.html')





#Login page
@app.route('/Login')
def Login():
    print('test Login page')
    return render_template("Login.html")



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)