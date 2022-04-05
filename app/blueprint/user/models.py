from app import db
from flask_login import UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=False,unique=True)
    password = db.Column(db.String(240), nullable=False)
    user_type = db.Column(db.String(30),nullable = False)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
