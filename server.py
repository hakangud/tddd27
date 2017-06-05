from flask import request, Flask, send_file, session
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from db_models import *
from initial_db import initial_db
import json
import os
from datetime import datetime, timedelta
from oauth2client import client, crypt
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x8fp\x16#Z\x0b\x81\xeb\x16')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localdb2.db'
db.init_app(app)
initial_db(app, db)

websockets = {}

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
    s.sendmail('myFridge', [email], msg.as_string())
    s.quit()

@app.route('/')
def init():
    return send_file('templates/index.html')

def check_best_before():
    with app.app_context():
        users = User.query.all()
        tomorrow = datetime.now() + timedelta(days=1)
        for user in users:
            groceries = []
            if user.fridge:
                groceries = user.fridge.get_all_groceries_in_fridge(convert_to_string = False)

            grocery_expires_tomorrow = list()
            for grocery in groceries:
                if datetime.date(grocery['best_before']) == datetime.date(tomorrow):
                    grocery_expires_tomorrow.append(str(grocery['name']))

            if grocery_expires_tomorrow:
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
            registered_user = User.query.filter_by(email=email).first()
            if registered_user is not None:
                user_id = registered_user.get_id()
                websockets[user_id] = ws

    return

@app.route('/googleauth', methods=['POST'])
def google_auth():
    try:
        data = json.loads(request.data.decode())
        idinfo = client.verify_id_token(data['data'], '192085420693-gnet8a4sjhn89ll6ejjho1tudv3l2oaa.apps.googleusercontent.com')
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        else:
            userid = idinfo['sub']
            registered_user = User.query.filter_by(email=idinfo['email']).first()
            if not registered_user:
                user = User(email=idinfo['email'])
                db.session.add(user)
                db.session.commit()
                registered_user = User.query.filter_by(email=idinfo['email']).first()

            return login_registered_user(registered_user)

    except crypt.AppIdentityError:
        return json.dumps({'message': 'Invalid token'}), 400

@app.route('/login', methods=['POST'])
def login():
    with app.app_context():
        data = json.loads(request.data.decode())
        email = data['email']
        password = data['password']
        registered_user = User.query.filter_by(email=email).first()
        if registered_user is not None and password is not None and registered_user.check_password(password):
            return login_registered_user(registered_user)
        else:
            return json.dumps({'message': 'Wrong email or password, try again'}), 400

def login_registered_user(registered_user):
    data = None
    has_fridge = False
    if registered_user.fridge:
        data = registered_user.fridge.get_all_groceries_in_fridge(convert_to_string = True)
        has_fridge = True

    user_id = registered_user.get_id()
    session['logged_in'] = True
    session['user_id'] = user_id
    return json.dumps({'message': 'You are now signed in', 'data': data, 'has_fridge': has_fridge}), 200

@app.route('/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return True

    else:
        return False

@app.route('/signout', methods=['POST'])
def sign_out():
    user_id = session['user_id']
    if status():
        del websockets[user_id]
        session.pop('logged_in', None)
        return json.dumps({'message': 'You are now signed out'}), 200
    else:
        return json.dumps({'message': 'You are not signed in'}), 400

@app.route('/register', methods=['POST'])
def register():
    with app.app_context():
            data = json.loads(request.data.decode())
            user = User(data['email'], data['password'], data['firstName'], data['lastName'], data['fridgeId'])
            registered_email = User.query.filter_by(email=user.email).first()
            user_fridge = Fridge.query.filter_by(id=user.fridge_id).first()
            if (registered_email is None):
                if user_fridge is not None:
                    db.session.add(user)
                    db.session.commit()
                    return json.dumps({"message": "You are now registered"}), 200
                else:
                    return json.dumps({"message": "Your fridge is not in our system"}), 400

            else:
                return json.dumps({"message": "The email is already in use"}), 400

@app.route('/addfridge', methods=['POST'])
def add_fridge():
    if status():
        with app.app_context():
            data = json.loads(request.data.decode())
            user = User.query.filter_by(id=session['user_id']).first()
            user.fridge_id = data
            db.session.add(user)
            db.session.commit()
            fridge = Fridge.query.filter_by(id=data).first()
            data = fridge.get_all_groceries_in_fridge(convert_to_string = True)
            return json.dumps({"message": "Fridge is added", "data": data}), 200

@app.route('/addgrocery', methods=['POST'])
def add_grocery_in_fridge():
    if status():
        with app.app_context():
            data = json.loads(request.data.decode())
            grocery = Grocery.query.filter_by(name=data['name']).first()
            fridge = Fridge.query.join(User).filter(User.id == session['user_id']).first()
            if grocery is not None:
                association = GroceriesInFridge.query.filter(GroceriesInFridge.grocery_id == grocery.id).filter(GroceriesInFridge.fridge_id == fridge.id).first()
                if association:
                    association.amount += int(data['amount'])
                else:
                    association = GroceriesInFridge(fridge, grocery, data['amount'], datetime.strptime(data['bestBefore'], '%Y-%m-%d'))

                db.session.add(association)
                db.session.commit()
                data = fridge.get_all_groceries_in_fridge(convert_to_string = True)
                ws = websockets[session['user_id']]
                ws.send(json.dumps({'action': 'updategroceries', 'message': 'Groceries updated', 'data': data}))
                return json.dumps({"message": "Grocery is added"}), 200
            else:
                return json.dumps({"message": "Grocery is not defined"}), 400

@app.route('/removegrocery', methods=['POST'])
def remove_grocery_in_fridge():
    if status():
        with app.app_context():
            data = json.loads(request.data.decode())
            grocery = Grocery.query.filter_by(name=data['name']).first()
            fridge = Fridge.query.join(User).filter(User.id == session['user_id']).first()
            if grocery and fridge is not None:
                association = GroceriesInFridge.query.filter(GroceriesInFridge.grocery_id == grocery.id).filter(GroceriesInFridge.fridge_id == fridge.id).first()
                if association is not None:
                    db.session.delete(association)
                    db.session.commit()
                    data = fridge.get_all_groceries_in_fridge(convert_to_string = True)
                    ws = websockets[session['user_id']]
                    ws.send(json.dumps({'action': 'updategroceries', 'message': 'Groceries updated', 'data': data}))
                    return json.dumps({"message": "Grocery is removed"}), 200
                else:
                    return json.dumps({"message": "Grocery is not in fridge"}), 400

            else:
                return json.dumps({"message": "Grocery is not defined"}), 400

@app.route('/getrecipes', methods=['GET'])
def get_recipes():
    if status():
        with app.app_context():
            fridge = Fridge.query.join(User).filter(User.id == session['user_id']).first()
            groceries_in_fridge = fridge.get_all_groceries_in_fridge(convert_to_string=False)
            grocery_names = [grocery['name'] for grocery in groceries_in_fridge]
            grocery_amount = [grocery['amount'] for grocery in groceries_in_fridge]
            fridge_dictionary = dict(zip(grocery_names, grocery_amount))
            recipes = Recipe.query.all()
            recipes_to_return = []
            for recipe in recipes:
                recipe_json = recipe.get_recipe()
                recipe_fridge_groceries = recipe.get_groceries(get_fridge_content=True)
                grocery_names_recipe = [grocery['name'] for grocery in recipe_fridge_groceries]
                grocery_amount_recipe = [grocery['amount'] for grocery in recipe_fridge_groceries]
                recipe_dictionary = dict(zip(grocery_names_recipe, grocery_amount_recipe))
                if set(grocery_names_recipe).issubset(set(grocery_names)):
                    recipe_amount_ok = True
                    for name in grocery_names_recipe:
                        if recipe_dictionary[name] > fridge_dictionary[name]:
                            recipe_amount_ok = False

                    if recipe_amount_ok:
                        recipes_to_return.append(recipe_json['title'])

            return json.dumps({'recipes': recipes_to_return}), 200

@app.route('/getrecipedetailed/<title>', methods=['GET'])
def get_recipe_detailed(title):
    if status():
        with app.app_context():
            recipe = Recipe.query.filter_by(title= title).first()
            print('recipe detailed')
            return json.dumps({'recipe_detailed': recipe.get_recipe()}),200

if __name__ == '__main__':
    http_server = WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()