from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

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
@app.route('/Signup')
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