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
    imgs = db.getPublicImages()
    if 'username' in session:
        user = session['username']
        insess = True
    else:
        user = ''
        insess = False
    return render_template('index.html', username=user, sess = insess, imgs = imgs)

@app.route('/logged', methods=['POST'])
def logged():
    imgs = db.getPublicImages()
    if request.method == 'POST':
        if db.login(request.form['username'], request.form['password']):
            print('Logged in')
            session['username'] = request.form['username']
            session['insession'] = True
            print("In session")
    if 'username' in session:
        user = session['username']
        insess = True
    else:
        user = ''
        insess = False
    return render_template('index.html', username=user, sess = insess, imgs = imgs)

@app.route('/signed', methods=['POST'])
def signed():
    imgs = db.getPublicImages()
    if request.method == 'POST':
        if db.checkExists(request.form['username']):
            print("Taken")
            return render_template('index.html')
        else:
            print("Done")
            session['username'] = request.form['username']
            session['insession'] = True
            db.addToUsers(request.form['username'], request.form['password'])
    if 'username' in session:
        user = session['username']
        insess = True
    else:
        user = ''
        insess = False
    return render_template('index.html', username=user, sess = insess, imgs = imgs)
    
@app.route('/signup')
def signup():
    return render_template('signup.html')
    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    imgs = db.getPublicImages()
    session.clear()
    insess = False
    return render_template('index.html', sess = insess, imgs = imgs)
    
@app.route('/upload')
def upload():
    if 'username' in session:
        user = session['username']
        insess = True
    else:
        user = ''
        insess = False
    return render_template('upload.html', sess = insess, username = user)
    
@app.route('/loaded', methods=['POST'])
def loaded():
    url = request.form['url']
    print(request.form['imgname'])
    print(request.form['public'])
    print(request.form['tags'])
    if request.method == 'POST':
        db.addToImages(request.form['url'], request.form['imgname'], session['username'], request.form['public'])
        x = db.splitText(request.form['tags'])
        for word in x:
            print(word)
            db.addToTags(url, word)
    if 'username' in session:
        user = session['username']
        insess = True
    else:
        user = ''
        insess = False
    imgs = db.getPublicImages()
    return render_template('index.html', sess = insess, imgs = imgs)

    
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        imgs = db.search(request.form['serch'])
    if 'username' in session:
        user = session['username']
        insess = True
    else:
        user = ''
        insess = False
    return render_template('index.html', sess = insess, imgs = imgs)

# start the server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)