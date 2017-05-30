from db_models import Fridge, User, Grocery, GroceriesInFridge, Recipe

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
        test_user = User('emelie.aspholm@hotmail.com', 'hej','Emelie','Aspholm', '1')
        db.session.add(test_user)

        test_user2 = User('hej@h', 'hej','Emelie','Aspholm', '2')
        db.session.add(test_user2)

        test_user3 = User('hakangud@gmail.com', 'a', 'Hakan', 'Gudmundsson', '1')
        db.session.add(test_user3)

        test_user4 =User(email='hej@hej')
        db.session.add(test_user4)

        db.session.commit()


        #test_user4.fridge_id = 4
        #db.session.add(test_user4)
        #db.session.commit()


        association3 = GroceriesInFridge(fridge_1, grocery_1, '200', datetime(2017, 05, 31))
        db.session.add(association3)

        association4 = GroceriesInFridge(fridge_2, grocery_1, '200', datetime(2017, 05, 31))
        db.session.add(association4)


        association = GroceriesInFridge(fridge_1, grocery_3, '200', datetime(2017, 05, 31))
        db.session.add(association)

        association2 = GroceriesInFridge(fridge_1, grocery_4, '200', datetime(2017, 05, 31))
        db.session.add(association2)



        db.session.commit()


        #db.session.delete(association2)
        #db.session.delete(association2)
        print('ass')
        print(association2)
        #query_grocery_in_fridge = Grocery.query.filter(GroceriesInFridge.grocery_id == 3 and GroceriesInFridge.fridge_id == 1).first()

        #print(.query(User).filter(User.keywords.any(keyword='jek')))
        query_grocery_in_fridge = Grocery.query.join(GroceriesInFridge).join(Fridge).filter(GroceriesInFridge.grocery_id == 4 and GroceriesInFridge.fridge_id == 1).first()

        query_assosiation = GroceriesInFridge.query.filter(GroceriesInFridge.grocery_id == 1 and GroceriesInFridge.fridge_id == 2).first()

        query_assosiation = GroceriesInFridge.query.filter(GroceriesInFridge.grocery_id == 4).filter(GroceriesInFridge.fridge_id == 1).first()
        print('here')
        print(query_assosiation)

        print(query_grocery_in_fridge)

        db.session.delete(query_assosiation)
        db.session.commit()




        tacopaj_course = Recipe(u"Tacopaj", 65, u"Blotlagg strobrodet i mjolken.")
        tacogryta_course = Recipe(u"Tacogryta", 70, u"Blotlagg strobrodet i mjolken och krydda grytan.")


        omelette_recipe = Recipe(u"Omelette", 15, u"Blotlagg strobrodet i mjolken.")
        # tacopaj_course.add_ingredient(butter_ingredient, 75, True)
        # tacopaj_course.add_ingredient(flour_ingredient, 2, True)
        # tacopaj_course.add_ingredient(graham_flour_ingredient, 1, True)
        # tacopaj_course.add_ingredient(sour_cream_ingredient, 3, True)
        # tacopaj_course.add_ingredient(minced_meat_ingredient, 500, True)
        # tacopaj_course.add_ingredient(taco_spicemix_ingredient, 40, True)
        # tacopaj_course.add_ingredient(taco_sauce_ingredient, 260, True)
        # tacopaj_course.add_ingredient(egg_ingredient, 2, True)
        # tacopaj_course.add_ingredient(aged_cheese_ingredient, 100, True)
        # tacopaj_course.add_ingredient(salt_ingredient, 2, False)
        # tacopaj_course.add_ingredient(pepper_ingredient, 3, False)

        tacopaj_course.add_grocery(grocery_3, 75, True)
        tacopaj_course.add_grocery(grocery_1, 2, True)

        tacogryta_course.add_grocery(grocery_3, 70, True)
        tacogryta_course.add_grocery(grocery_1, 1, True)
        #tacopaj_course.add_grocery(grocery_2, 1, True)
        #tacopaj_course.add_grocery(grocery_4, 3, True)
        db.session.add(tacopaj_course)
        db.session.add(tacogryta_course)
        db.session.commit()