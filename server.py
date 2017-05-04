from flask import request, Flask
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import json

app = Flask(__name__, static_folder='login')

@app.route('/')
def hello():
    return app.send_static_file('login.view.html')

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

if __name__ == '__main__':
    http_server = WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    app.run()