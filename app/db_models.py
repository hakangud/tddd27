import json
from datetime import datetime


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(100), unique=True, index=True)
    password = db.Column('password', db.String(100))
    name = db.Column('name', db.String(100))
    fridge = db.Column('email', db.String(100), unique=True)
    registered_on = db.Column('registered_on', db.DateTime)


    def __init__(self, email=None, password=None, name=None, fridge=None):
        self.email = email
        self.password = password
        self.name = name
        self.fridge = fridge
        self.registered_on = datetime.utcnow()