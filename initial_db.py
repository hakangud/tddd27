from db_models import Fridge, User, Grocery

from datetime import datetime

def initial_db(app, db):
    with app.app_context():

        db.drop_all()
        db.create_all()
        db.session.commit()

        #INITIATE DB WITH GROCERIES
        grocery_1 = Grocery(u"Tomato")
        db.session.add(grocery_1)
        grocery_2 = Grocery(u"Milk")
        db.session.add(grocery_2)
        grocery_3 = Grocery(u"Sour cream")
        db.session.add(grocery_3)
        grocery_4 = Grocery(u"Cheese")
        db.session.add(grocery_4)
        grocery_5 = Grocery(u"Ham")
        db.session.add(grocery_5)

        #INITIATE DB WITH FRIDGES AND ADD GROCERIES
        fridge_1 = Fridge(u"Super fridge")
        fridge_1.add_grocery(grocery_1, '100', datetime(2017, 05, 31))
        fridge_1.add_grocery(grocery_2, '1', datetime(2017, 06, 01))
        db.session.add(fridge_1)
        fridge_2 = Fridge(u"My fridge")
        db.session.add(fridge_2)






        #INITIATE DB WITH USERS
        test_user = User('hej@hej', 'hej','Emelie','Aspholm','1')
        db.session.add(test_user)

        db.session.commit()




