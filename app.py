from flask import Flask, render_template

app = Flask(__name__)

#Landing page
@app.route('/')
def landing():
    print('test landing page')
    return render_template('Home.html')

#Home page return
@app.route('/Home')
def home():
    print('test home return')
    return render_template("Home.html")

#Infomation page
@app.route('/Infomation')
def infomation():
    print('test infomation')
    return render_template("Infomation.html")

#About page
@app.route('/About')
def about():
    print('test about page')
    return render_template('About.html')

#Login page
@app.route('/Login')
def Login():
    print('test Login page')
    return render_template("Login.html")



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)