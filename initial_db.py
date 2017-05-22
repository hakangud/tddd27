from db_models import Fridge, User

def initial_db(app, db):
    with app.app_context():

        db.drop_all()
        db.create_all()
        db.session.commit()


        #INITIATE DB WITH FRIDGES TEMPORARY SOLUTION FOR TESTING BELOW
        fridge_1 = Fridge(u"Super fridge")
        db.session.add(fridge_1)
        fridge_2 = Fridge(u"My fridge")
        db.session.add(fridge_2)

        test_user = User('hej@hej', 'hej','Emelie','Aspholm','2')
        db.session.add(test_user)

        db.session.commit()




