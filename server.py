from flask import request, Flask, send_file, g, session
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from db_models import *
from initial_db import initial_db
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime, timedelta

from googleapiclient import discovery
import httplib2
from oauth2client import client, crypt
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x8fp\x16#Z\x0b\x81\xeb\x16')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localdb2.db'

db.init_app(app)
initial_db(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

websockets = {}

# session.clear()

def send_email(email, data):
    text = ""
    for s in data:
        text += s + ", "

    text = text[:-2]
    msg = MIMEText("Your groceries: " + text + " expires tomorrow.")
    msg['Subject'] = 'Groceries expires'
    msg['From'] = 'myFridge'
    msg['To'] = email

    s = smtplib.SMTP('localhost')
    print "sending email"
    s.sendmail('myFridge', [email], msg.as_string())
    print "email sent"
    s.quit()

@login_manager.user_loader
def load_user(id):
    print("du er her")
    print(id)
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def init():
    return send_file('templates/index.html')

# @app.route('/login', methods=['POST'])
# def login():
#     user=g.user
#     print(user.__repr__())
#     with app.app_context():
#         data = json.loads(request.data.decode())
#
#         email = data['email']
#         password = data['password']
#         #registered_user = User.query.filter_by(email='eme.asp@hej.com', password='hej').first()
#         registered_user = User.query.filter_by(email=email, password=password).first()
#         #logout_user()
#         if registered_user is None:
#             print "user is none"
#             return json.dumps({'message': 'Wrong email or password, try again'}), 400
#
#         #if current_user.is_authenticated():
#         #    print('authentivatetd before login')
#
#         if user.is_authenticated:
#             print('authentivatetd before login not funcion')
#
#         #if current_user.is_active():
#         #    print('active before login')
#
#         if current_user.is_active:
#             print('active before login not funcion')
#
#
#         print(current_user.__repr__())
#
#         login_user(registered_user)
#         print(current_user.__repr__())
#         #return groceries in the users fridge
#         data = '1qaz2wsdx3edc'
#
#         if current_user.is_authenticated:
#             print('yes')
#             return json.dumps({'message': 'You are now signed in', 'data': data}), 200
#         else:
#             print('nope')

def check_best_before():
    with app.app_context():
        users = User.query.all()
        tomorrow = datetime.now() + timedelta(days=1)

        for user in users:
            groceries = user.fridge.get_all_groceries_in_fridge(convert_to_string = False)
            grocery_expires_tomorrow = list()
            for grocery in groceries:
                if datetime.date(grocery['best_before']) == datetime.date(tomorrow):
                    grocery_expires_tomorrow.append(str(grocery['name']))
            print('grocery expires tomorrow')
            print(grocery_expires_tomorrow)

            if grocery_expires_tomorrow:
                print(user.email)
                print(grocery_expires_tomorrow)
                send_email(str(user.email), grocery_expires_tomorrow)


def get_user_id(email):
    registered_user = User.query.filter_by(email=email).first()
    user_id = registered_user.get_id()
    return user_id

@app.route('/websocket')
def websocket():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            email = json.loads(ws.receive())['data']
            print "email is"
            print email
            registered_user = User.query.filter_by(email=email).first()
            print "registered user is"
            print registered_user
            if registered_user is not None:
                print "user_id1 is"
                user_id = registered_user.get_id()
                print user_id
                websockets[user_id] = ws

    return

@app.route('/googleauth', methods=['POST'])
def google_auth():
    try:
        data = json.loads(request.data.decode())
        idinfo = client.verify_id_token(data['data'], '192085420693-gnet8a4sjhn89ll6ejjho1tudv3l2oaa.apps.googleusercontent.com')
        print idinfo['name']
        print idinfo['email']

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")

        else:
            print "token ok"
            userid = idinfo['sub']
            return json.dumps({'success': True, 'message': 'You are now signed in'}), 200

    except crypt.AppIdentityError:
        print "invalid token"
        return json.dumps({'success': True, 'message': 'Invalid token'}), 400



@app.route('/login', methods=['POST'])
def login():
    print(status())
    with app.app_context():
        data = json.loads(request.data.decode())

        email = data['email']
        password = data['password']
        #registered_user = User.query.filter_by(email='eme.asp@hej.com', password='hej').first()
        registered_user = User.query.filter_by(email=email).first()



        if registered_user is not None and registered_user.check_password(password):

            data = None

            if registered_user.fridge:
                data = registered_user.fridge.get_all_groceries_in_fridge(convert_to_string = True)
                user_id = registered_user.get_id()


            session['logged_in'] = True
            session['user_id'] = user_id
            print(status())
            print(session)

            return json.dumps({'message': 'You are now signed in', 'data': data}), 200
        else:
            return json.dumps({'message': 'Wrong email or password, try again'}), 400



@app.route('/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return True
    else:
        return False


@app.route('/signup', methods=['POST'])
def sign_up():
    return json.dumps({'message': 'You are now signed up'}), 200

@app.route('/signout', methods=['POST'])
#@login_required
def sign_out():
    #logout_user()
    # websocket test
    user_id = session['user_id']
    print "user_id2 is"
    print user_id

    print('signout was visited')
    if status():
        del websockets[user_id]
        session.pop('logged_in', None)
        return json.dumps({'message': 'You are now signed out'}), 200
    else:
        return json.dumps({'message': 'You are not signed in'}), 400

@app.route('/register', methods=['POST'])
def register():
    print(current_user.__repr__())
    with app.app_context():
            data = json.loads(request.data.decode())
            #user = User('emesasa.asp@hej.com', 'hej','Emelie','Aspholm','2')

            user = User(data['email'], data['password'], data['firstName'], data['lastName'], data['fridgeId'])
            registered_email = User.query.filter_by(email=user.email).first()
            user_fridge = Fridge.query.filter_by(id=user.fridge_id).first()
            #if (registered_email is None) and (not (validate_email(request.form['regEmail']))):
            if (registered_email is None):
                if user_fridge is not None:
                    db.session.add(user)
                    db.session.commit()
                    print(session.__repr__())
                    return json.dumps({"message": "You are now registered"}), 200
                else:
                    return json.dumps({"message": "Your fridge is not in our system"}), 400
            else:
                return json.dumps({"message": "The email is already in use"}), 400



@app.route('/addgrocery', methods=['POST'])
def add_grocery_in_fridge():
    if status():
        print(session)
        with app.app_context():
            data = json.loads(request.data.decode())
            grocery = Grocery.query.filter_by(name=data['name']).first()
            user = User.query.filter_by(id=session['user_id']).first()

            fridge = Fridge.query.filter_by(id=user.fridge_id).first()
            print(fridge)
            if grocery is not None:
                association = GroceriesInFridge.query.filter(GroceriesInFridge.grocery_id == grocery.id and GroceriesInFridge.fridge_id == fridge.id).first()
                if association:
                    print(association.amount)
                    association.amount += int(data['amount'])
                    print(association.amount)
                else:
                    association = GroceriesInFridge(fridge, grocery, data['amount'], datetime.strptime(data['bestBefore'], '%Y-%m-%d'))
                db.session.add(association)
                db.session.commit()
                data = user.fridge.get_all_groceries_in_fridge(convert_to_string = True)
                print session['user_id']
                print websockets
                print 'DATA'
                print data
                ws = websockets[session['user_id']]
                ws.send(json.dumps({'action': 'updategroceries', 'message': 'Groceries updated', 'data': data}));
                return json.dumps({"message": "Grocery is added"}), 200
            else:
                return json.dumps({"message": "Grocery is not defined"}), 400




@app.route('/removegrocery', methods=['POST'])

def remove_grocery_in_fridge():
    if status():
        print(session)
        with app.app_context():
            data = json.loads(request.data.decode())

            grocery = Grocery.query.filter_by(name=data['name']).first()
            user = User.query.filter_by(id=session['user_id']).first()
            fridge = Fridge.query.filter_by(id=user.fridge_id).first()

            if grocery and fridge is not None:
                association = GroceriesInFridge.query.filter(GroceriesInFridge.grocery_id == grocery.id and GroceriesInFridge.fridge_id == fridge.id).first()
                if association is not None:
                    db.session.delete(association)
                    db.session.commit()
                    data = user.fridge.get_all_groceries_in_fridge(convert_to_string = True)
                    ws = websockets[session['user_id']]
                    ws.send(json.dumps({'action': 'updategroceries', 'message': 'Groceries updated', 'data': data}));
                    return json.dumps({"message": "Grocery is removed"}), 200
                else:
                    return json.dumps({"message": "Grocery is not in fridge"}), 400
            else:
                return json.dumps({"message": "Grocery is not defined"}), 400



@app.route('/getrecipes', methods=['GET'])
def get_recipes():
    if status():
        print(session)
        with app.app_context():
            #data = json.loads(request.data.decode())

            user = User.query.filter_by(id=session['user_id']).first()
            fridge = Fridge.query.filter_by(id=user.fridge_id).first()
            groceries_in_fridge = fridge.get_all_groceries_in_fridge(convert_to_string=False)
            grocery_names = [grocery['name'] for grocery in groceries_in_fridge]
            grocery_amount = [grocery['amount'] for grocery in groceries_in_fridge]
            fridge_dictionary = dict(zip(grocery_names, grocery_amount))

            print('grocery_names')
            print(grocery_names)

            recipes = Recipe.query.all()
            recipes_to_return = []
            for recipe in recipes:
                recipe_json = recipe.get_recipe()
                recipe_fridge_groceries = recipe.get_groceries(get_fridge_content=True)
                grocery_names_recipe = [grocery['name'] for grocery in recipe_fridge_groceries]
                grocery_amount_recipe = [grocery['amount'] for grocery in recipe_fridge_groceries]
                recipe_dictionary = dict(zip(grocery_names_recipe, grocery_amount_recipe))

                print('grocery_names_recipe')
                print(grocery_names_recipe)


                if set(grocery_names_recipe).issubset(set(grocery_names)):
                    recipe_amount_ok = True
                    for name in grocery_names_recipe:
                        if recipe_dictionary[name] > fridge_dictionary[name]:
                            recipe_amount_ok = False
                        #print(groceries_in_fridge)
                        #print(recipe_fridge_groceries[i]['amount'])
                    if recipe_amount_ok:
                        recipes_to_return.append(recipe_json['title'])


                #print(recipe_fridge_groceries)
            print('recipes_to_return')
            print(recipes_to_return)
            return json.dumps({'recipes': recipes_to_return}), 200

@app.route('/getrecipedetailed/<title>', methods=['GET'])
def get_recipe_detailed(title):
    if status():
        with app.app_context():
            recipe = Recipe.query.filter_by(title= title).first()
            print('recipe detailed')
            return json.dumps({'recipe_detailed': recipe.get_recipe()}),200




def test_user():
    with app.app_context():
        # user = User('hej@hej','hej','Emelie','Aspholm','2')
        # db.session.add(user)
        #
        # db.session.commit()
        fridges = Fridge.query.all()

        print(fridges[0].user)
        id = fridges[0].get_fridge_id()
        print(id)

            # Method for adding a fridge to the user. Returns ...
    #def add_fridge(self, this_fridge):
        users = User.query.all()
        print(users[0].id)
        #users[0].fridge_id = fridges[0].id

        db.session.add(users[0])
        #db.session.flush()
        db.session.commit()
        print("hej")
        #return ''

        users = User.query.all()
        if users[0].fridge:
            user_id = users[0].fridge.get_fridge_id()

        data = users[0].fridge.get_all_groceries_in_fridge()

        print(data)
        print('user_id:')
        print(user_id)
        print(current_user.__repr__())
        return fridges

#test_user()
#login()
#print(register())
#add_grocery_in_fridge()

#check_best_before()
#get_recipes()

if __name__ == '__main__':
    http_server = WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

    #app.run(host='127.1.1.3')