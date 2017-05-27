from db_models import Fridge, User, Grocery, GroceriesInFridge

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
        #fridge_1.add_grocery(grocery_1, '100', datetime(2017, 05, 31))
        #fridge_1.add_grocery(grocery_2, '1', datetime(2017, 06, 01))
        db.session.add(fridge_1)



        fridge_2 = Fridge(u"My fridge")
        db.session.add(fridge_2)






        #INITIATE DB WITH USERS
        test_user = User('hej@hej', 'hej','Emelie','Aspholm', '1')
        db.session.add(test_user)

        test_user2 = User('hej@h', 'hej','Emelie','Aspholm', '2')
        db.session.add(test_user2)


        db.session.commit()

        association = GroceriesInFridge(fridge_1, grocery_3, '200', datetime(2017, 05, 31))
        db.session.add(association)

        association2 = GroceriesInFridge(fridge_1, grocery_4, '200', datetime(2017, 05, 31))
        db.session.add(association2)

        db.session.commit()



        query_grocery_in_fridge = Grocery.query.join(GroceriesInFridge).join(Fridge).filter(GroceriesInFridge.grocery_id == 3 and GroceriesInFridge.fridge_id == 1).first()
        print(query_grocery_in_fridge)
        #db.session.delete(query_grocery_in_fridge)
        #db.session.commit()