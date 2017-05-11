import json
from datetime import datetime


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = "user"
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(100), unique=True, index=True)
    password = db.Column('password', db.String(100))
    name = db.Column('name', db.String(100))
    last_name = db.Column('last_name', db.String(100))
    #fridge = db.Column('number', db.String(100), unique=True)
    registered_on = db.Column('registered_on', db.DateTime)
    fridge_id = db.Column('fridge', db.Integer, db.ForeignKey('fridge.fridge_id'))

    user = db.relationship('Fridge')


    def __init__(self, email=None, password=None, name=None, last_name= None, fridge=None):
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        self.fridge_id = fridge
        self.registered_on = datetime.utcnow()




class Fridge(db.Model):
    __tablename__ = "fridge"
    id = db.Column('fridge_id', db.Integer, primary_key=True)
    model_name = db.Column('model_name', db.String(100))
    #grocery_array = [{kind: 'tomat',best_before: 2012-03-02},{kind: 'gurka', best_before: 2012-02-12}]
    groceries_in_fridge = ('groceries_in_fridge', db.JSON())
    #users = db.relationship('User')


    def __init__(self, model_name=None, groceries_in_fridge=None):
        self.model_name = model_name
        self.groceries_in_fridge = json.dumps(groceries_in_fridge)



    def get_fridge_id(self):
        #return self.id
        return self.id
#
# class Grocery(db.Model):
#     __tablename__ = "groceries"
#     id = db.Column('grosseary_id', db.Integer, primary_key=True)
#     name = db.Column('name', db.String(100))
#
#     def __init__(self, model_name=None,date = None):
#         self.model_name = model_name


