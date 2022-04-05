from app import db


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phoneNo = db.Column(db.String(80), nullable=False)
