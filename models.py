from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(6), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False, default=18)
    hypertension = db.Column(db.Boolean, default=False, nullable=False)
    heart_disease = db.Column(db.Boolean, default=False, nullable=False)
    ever_married = db.Column(db.String(3), unique=True, nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'
