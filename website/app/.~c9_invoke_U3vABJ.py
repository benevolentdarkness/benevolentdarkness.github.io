import os
import uuid
from flask.ext.socketio import SocketIO, emit
import database as db
from jinja2 import Template
from flask import Flask, render_template, url_for, request, session;
app = Flask(__name__)


app.secret_key = os.urandom(24).encode('hex')
admin = False
owner = False

@app.route('/')
def mainIndex():
    main = True
    typo = False
    other = False
    log = False
    digital = False
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    #print(photoLink)
    return render_template('index.html', user=user, sess=insession, main=main)

@app.route('/typography')
def mainTypo():
    main = False
    typo = True
    other = False
    log = False
    digital = False
    typoLib = [{'file':'Image01.jpeg',
    'title': '13 Years Old'},
    {'file':'Image02.jpeg',
    'title': 'Triggered'},
    {'file': 'Image03.jpeg',
    'title': 'Comment Below'},
    {'file': 'Image04.jpeg',
    'title': 'Rule 71'}]
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    return render_template('page2.html', images=typoLib, user=user, sess=insession, typo=typo)
    
@app.route('/about')
def mainAbout():
    main = False
    typo = False
    other = False
    log = False
    digital = False
    selfie = "selfie.jpeg"
    alias = True
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    return render_template('page3.html', image=selfie, name=alias, user=user, sess=insession)
    
@app.route('/suggestions')
def mainSuggest():
    main = False
    typo = False
    other = False
    log = False
    digital = False
    check = db.executeQuery("SELECT username, suggestiontype, suggestion, votes FROM suggestions INNER JOIN users ON suggestions.userid = users.userid", db.connectMaster())
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    return render_template('SuggestionPage.html', tab=check, user=user, sess=insession)
    
@app.route('/suggestions/suggest')
def mainSuggestions():
    #test = url_for('thankyou')
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
    else:
        insession = False
        user = ['', '', '', 0]
    return render_template('suggestion.html', user=user, sess=insession)
    
@app.route('/thankyou', methods=['POST'])
def test():
    main = False
    typo = False
    other = False
    log = False
    digital = False
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    sugty = request.form['sugtype']
    sug = request.form['sug']
    userid = db.executeQuery("SELECT userid FROM users WHERE username='%s'" % (user[0]), db.connectUsers())
    db.addToSuggestions(userid, sugty, sug)
    return render_template('thankyou.html', user=user, sess=insession)
    
@app.route('/create_account')
def mainCreate():
    main = False
    typo = False
    other = False
    log = True
    digital = False
    return render_template('createaccount.html', log=log)
    
@app.route('/logged', methods=['POST'])
def mainLogged():
    main = False
    typo = False
    other = False
    log = False
    digital = False
    if request.method == 'POST':
        if db.checkexists(db.connectUsers(), request.form['username']):
            print("Taken")
            return render_template('usernametaken.html')
        else:
            print("Done")
            session['username'] = request.form['username']
            session['firstname'] = request.form['firstname']
            session['lastname'] = request.form['lastname']
            session['admin'] = db.getAdmin(session['username'], db.connectUsers())
            db.addToUsers(request.form['firstname'], request.form['lastname'], request.form['username'], request.form['age'], request.form['pw'], request.form['email'])
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    return render_template('index.html', sess=insession, user=user)
    
@app.route('/login', methods=['POST'])
def mainIn():
    if request.method == 'POST':
        if db.checkexists(db.connectUsers(), request.form['username']):
            if db.matchpassword(db.connectUsers(), request.form['pw'], request.form['username']):
                session['username'] = request.form['username']
                session['firstname'] = db.executeQuery("SELECT firstname FROM users WHERE username='%s'" % (request.form['username']), db.connectUsers())
                session['lastname'] = db.executeQuery("SELECT lastname FROM users WHERE username='%s'" % (request.form['username']), db.connectUsers())
                session['admin'] = db.getAdmin(session['username'], db.connectUsers())
                print("Logged in")
            else:
                print("Incorrect password")
        else:
            print("Incorrect username")
            
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    return render_template('index.html', sess=insession, user=user)
    
@app.route('/logout')
def mainOut():
    session.clear()
    insession = False
    return render_template('index.html', sess=insession)
    
@app.route('/suggestions/sort', methods=['POST'])
def mainSort():
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    sort = [request.form['search']]
    name = user[0]
    print(name)
    query = "SELECT username, suggestiontype, suggestion, votes FROM users INNER JOIN suggestions ON users.userid = suggestions.userid"
    if request.form['own'] == 'false':
        query += " ORDER BY %s"
        check = db.sort(query, sort)
        print(check)
        return render_template('SuggestionPage.html', tab=check, user=user, sess=insession)
    else:
        query += " WHERE username=%s"
        query += " ORDER BY %s"
        check = db.sortOwn(query, name, sort)
        print(check)
        return render_template('SuggestionPage.html', tab=check, user=user, sess=insession)
        
@app.route('/chat')
def mainChat():
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], session['admin']]
        if session['admin'] >= 1:
            admin = True
        if session['admin'] == 2:
            owner = True
    else:
        insession = False
        user = ['', '', '', 0]
    return render_template('chat.html', user=user, sess=insession)

# start the server
if __name__ == '__main__':
   app.run(app, host='0.0.0.0', port=8080)
