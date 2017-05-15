from flask import request, Flask, send_file
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from db_models import *
from initial_db import initial_db
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.debug = True


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localdb2.db'

db.init_app(app)



initial_db(app, db)

@app.route('/')
def hello():
    return send_file('templates/index.html')

@app.route('/signin', methods=['POST'])
def login():
    data = '1qaz2wsdx3edc'
    return json.dumps({'success': True, 'message': 'You are now signed in', 'data': data})

@app.route('/signup', methods=['POST'])
def sign_up():
    return json.dumps({'success': True, 'message': 'You are now signed up'})

@app.route('/signout', methods=['POST'])
def sign_out():
    return json.dumps({'success': True, 'message': 'You are now signed out'})


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     user = User(request.form['regEmail'], request.form['regPassword'],request.form['regName'], request.form['regFridge'])
#     registered_email = User.query.filter_by(email=user.email).first()
#     user_fridge = Fridge.query.filter_by(id=user.fridge).first()
#
#
#     #if (registered_email is None) and (not (validate_email(request.form['regEmail']))):
#     if (registered_email is None):
#         if user_fridge is not None:
#             db.session.add(user)
#             db.session.commit()
#         else:
#             return json.dumps({"success": False, "message": "Your fridge is not in our system"})
#     return json.dumps({"success": True, "message": "You are now registered"})
#

def test_user():
    with app.app_context():
        user = User('eme.asp@hej.com', 'hej','Emelie','Aspholm','2')
        db.session.add(user)

        db.session.commit()
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

        print(user_id)
        return fridges

test_user()


if __name__ == '__main__':
    http_server = WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    #app.run(host='127.1.1.3')


