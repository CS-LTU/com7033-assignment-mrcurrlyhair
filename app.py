from flask import Flask, render_template

app = Flask(__name__)

@app.route('/Home')
def home():
    return render_template("Home.html")

@app.route('/About')
def about():
    return render_template("About.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)