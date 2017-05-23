from flask import request, Flask, send_file, g, session
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from db_models import *
from initial_db import initial_db
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
import json
import os


app = Flask(__name__)
app.debug = True

#TODO: move to a file
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x8fp\x16#Z\x0b\x81\xeb\x16')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localdb2.db'

db.init_app(app)
initial_db(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

# session.clear()

@login_manager.user_loader
def load_user(id):
    print("du er her")
    print(id)
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def hello():
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


@app.route('/login', methods=['POST'])
def login():
    print(status())
    with app.app_context():
        data = json.loads(request.data.decode())

        email = data['email']
        password = data['password']
        #registered_user = User.query.filter_by(email='eme.asp@hej.com', password='hej').first()
        registered_user = User.query.filter_by(email=email).first()



    data = '1qaz2wsdx3edc'

    if registered_user is not None and registered_user.check_password(password):
        session['logged_in'] = True
        print(status())
        session.pop('logged_in', None)
        print(status())
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
    if status():
        session.pop('logged_in', None)
    return json.dumps({'message': 'You are now signed out'}), 200

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(current_user.__repr__())
    with app.app_context():
            data = json.loads(request.data.decode())
            #user = User('emesasa.asp@hej.com', 'hej','Emelie','Aspholm','2')
            #TODO: store crypted password
            user = User(data['email'], data['password'], data['firstName'], data['lastName'], data['fridgeId'])
            registered_email = User.query.filter_by(email=user.email).first()
            user_fridge = Fridge.query.filter_by(id=user.fridge_id).first()
            #if (registered_email is None) and (not (validate_email(request.form['regEmail']))):
            if (registered_email is None):
                if user_fridge is not None:
                    db.session.add(user)
                    db.session.commit()
                    print(current_user.__repr__())
                    return json.dumps({"message": "You are now registered"}), 200
                else:
                    return json.dumps({"message": "Your fridge is not in our system"}), 400
            else:
                return json.dumps({"message": "The email is already in use"}), 400


def test_user():
    with app.app_context():
        # user = User('hej@hej','hej','Emelie','Aspholm','2')
        # db.session.add(user)
        #
        # db.session.commit()
        fridges = Fridge.query.all()


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
        user_id = users[0].fridge.get_fridge_id()

        data = users[0].fridge.get_all_groceries_in_fridge()

        print(data)
        print(user_id)
        print(current_user.__repr__())
        return fridges

test_user()
#login()
#print(register())

if __name__ == '__main__':
    http_server = WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

    #app.run(host='127.1.1.3')