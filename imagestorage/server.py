import os
from flask.ext.socketio import SocketIO, emit
import database as db
from jinja2 import Template
from flask import Flask, render_template, url_for, request, session;
app = Flask(__name__)

socketio = SocketIO(app)
app.secret_key = os.urandom(24).encode('hex')

@app.route('/')
def mainIndex():
    return render_template('index.html')

# start the server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)