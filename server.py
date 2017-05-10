from flask import request, Flask, send_file
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from db_models import *
from initial_db import initial_db
import json

app = Flask(__name__)
app.debug = True
#db.init_app(app)



#populate_db(app, db)

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

if __name__ == '__main__':
    http_server = WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    #app.run(host='127.1.1.3')