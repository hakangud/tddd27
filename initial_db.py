from db_models import Fridge

def initial_db(app, db):
    with app.app_context():

        db.drop_all()
        db.create_all()
        db.session.commit()


        #INITIATE DB WITH FRIDGES TEMPORARY SOLUTION FOR TESTING BELOW
        fridge_1 = Fridge(u"Super fridge", "[{kind: 'tomat',best_before: 2012-03-02},{kind: 'gurka', best_before: 2012-02-12}]")
        db.session.add(fridge_1)
        fridge_2 = Fridge(u"My fridge", "[{kind: 'tomat',best_before: 2012-03-02},{kind: 'gurka', best_before: 2012-02-12}]")
        db.session.add(fridge_2)

        db.session.commit()


