import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, \
     check_password_hash



db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(100), unique=True, index=True)
    pw_hash = db.Column('password', db.String(100))
    name = db.Column('name', db.String(100))
    last_name = db.Column('last_name', db.String(100))
    #fridge = db.Column('number', db.String(100), unique=True)
    registered_on = db.Column('registered_on', db.DateTime)
    #fridge_id = db.Column('fridge_id', db.Integer, db.ForeignKey('fridge.fridge_id'))
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.fridge_id'))
    #fridge_id = db.relationship('Fridge', back_populates="user")

    fridge = db.relationship('Fridge')


    def __init__(self, email=None, password=None, name=None, last_name= None, fridge_id=None):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.fridge_id = fridge_id
        self.registered_on = datetime.utcnow()
        self.set_password(password)


    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


    # def is_active(self):
    #     return True
    #
    # def get_id(self):
    #     return unicode(self.id)
    #
    #
    # def is_authenticated(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False

    def __repr__(self):
        return '<User %r>' % (self.email)

        #this_fridge = Fridge.query.filter_by(id = fridge_id).first()
        #if fridge_id is not None and this_fridge is not None:

            #self.add_fridge(this_fridge)




    # # Method for adding a fridge to the user. Returns ...
    # def add_fridge(self, this_fridge):
    #
    #     self.fridge_id = this_fridge
    #     session.add(self)
    #     db.session.commit()
    #     return ''




class Fridge(db.Model):
    __tablename__ = "fridge"
    id = db.Column('fridge_id', db.Integer, primary_key=True)
    model_name = db.Column('model_name', db.String(100))
    #groceries_in_fridge = ('groceries_in_fridge', db.JSON())
    #users = db.relationship('User')
    user_id = db.relationship('User')
    groceries = db.relationship("GroceriesInFridge", back_populates="fridge")

    def __init__(self, model_name=None):
        self.model_name = model_name
        #self.groceries_in_fridge = json.dumps(groceries_in_fridge)


    def get_fridge_id(self):
        #return self.id
        return self.id


    # Method for adding an existing Grocery to this Fridge. The relationship attributes as the last two parameters
    def add_grocery(self, grocery, amount, best_before):
        association = GroceriesInFridge(amount=amount, best_before=best_before)
        association.grocery = grocery
        self.groceries.append(association)
        db.session.add(association)
        return ''


    def get_all_groceries_in_fridge(self):
        grocery_list = []
        for x in self.groceries:
            grocery_list.append({'name': x.grocery.name, 'amount': x.amount, 'best_before': x.best_before})
        return grocery_list


    def __repr__(self):
        return self.model_name

class Grocery(db.Model):
    __tablename__ = "groceries"
    id = db.Column('grocery_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    fridge = db.relationship("GroceriesInFridge", back_populates="grocery")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name


class GroceriesInFridge(db.Model):
    __tablename__ = "groceries_in_fridge"

    #id = db.Column ('id', db.Integer, primary_key=True)
    fridge_id = db.Column (db.Integer, db.ForeignKey('fridge.fridge_id'), primary_key=True)
    grocery_id = db.Column (db.Integer, db.ForeignKey('groceries.grocery_id'), primary_key=True)
    amount = db.Column('amount', db.Integer)
    best_before = db.Column('best_before', db.DateTime)
    #title = db.Column('title', db.String(100))
    fridge = db.relationship("Fridge", back_populates="groceries")
    grocery = db.relationship("Grocery", back_populates="fridge")


    def __repr__(self):
        return "".join((self.fridge.__repr__(),", ",self.grocery.__repr__()))

