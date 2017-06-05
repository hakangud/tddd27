from db_models import Fridge, User, Grocery, GroceriesInFridge, Recipe
from datetime import datetime

#INIATE DB WITH RECIPES, TEST USERS, FRIDGES AND GROCERIES
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
        egg_grocery = Grocery(u"Egg")
        db.session.add(egg_grocery)
        salt_grocery = Grocery(u"Salt")
        db.session.add(salt_grocery)
        pepper_grocery = Grocery(u"Pepper")
        db.session.add(pepper_grocery)

        #INITIATE DB WITH FRIDGES
        fridge_1 = Fridge(u"Super fridge")
        db.session.add(fridge_1)
        fridge_2 = Fridge(u"My fridge")
        db.session.add(fridge_2)

        #INITIATE DB WITH TEST USERS
        test_user = User('emelie.aspholm@hotmail.com', 'hej','Emelie','Aspholm', '1')
        db.session.add(test_user)
        test_user2 = User('hej@h', 'hej','Emelie','Aspholm', '2')
        db.session.add(test_user2)
        test_user3 = User('hakangud@gmail.com', 'a', 'Hakan', 'Gudmundsson', '1')
        db.session.add(test_user3)
        db.session.commit()

        #INITIATE FRIDGES WITH GROCERIES
        association = GroceriesInFridge(fridge_1, grocery_3, '200', datetime(2017, 06, 01))
        db.session.add(association)
        association2 = GroceriesInFridge(fridge_1, grocery_4, '200', datetime(2017, 06, 01))
        db.session.add(association2)
        association3 = GroceriesInFridge(fridge_1, grocery_1, '200', datetime(2017, 06, 01))
        db.session.add(association3)
        association4 = GroceriesInFridge(fridge_2, grocery_1, '200', datetime(2017, 06, 01))
        db.session.add(association4)
        db.session.commit()

        #INITIATE DB WITH RECIPE AND GROCERY CONNECTIONS
        tacopie_recipe = Recipe(u"Taco pie", 65, u"Heat oven to 400F.Grease 9-inch pie plate. Cook ground beef and onion in 10-inch skillet over medium heat, stirring occasionally, until beef is brown, drain. Stir in seasoning mix (dry). Spoon into pie plate, top with chilies.")
        tacopie_recipe.add_grocery(salt_grocery, 2, False)
        tacopie_recipe.add_grocery(pepper_grocery, 3, False)
        tacopie_recipe.add_grocery(grocery_3, 75, True)
        tacopie_recipe.add_grocery(grocery_1, 2, True)
        db.session.add(tacopie_recipe)

        taco_recipe = Recipe(u"Taco", 70, u"Heat oven to 400F. Grease 9-inch pie plate.")
        taco_recipe.add_grocery(grocery_3, 70, True)
        taco_recipe.add_grocery(grocery_1, 1, True)
        db.session.add(taco_recipe)

        omelette_recipe = Recipe(u"Omelette", 15, u"Crack the warm eggs into a bowl, add salt and blend with a fork. Heat a 10-inch nonstick aluminum pan over medium-high heat. Once the pan is hot, add the butter and brush around the surface of the pan. Pour the eggs into the center of the pan and stir vigorously with a rubber spatula for 5 seconds.")
        omelette_recipe.add_grocery(egg_grocery, 3, True)
        omelette_recipe.add_grocery(grocery_2, 3, True)
        omelette_recipe.add_grocery(salt_grocery, 2, False)
        omelette_recipe.add_grocery(pepper_grocery, 3, False)
        db.session.add(omelette_recipe)

        db.session.commit()