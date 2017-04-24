import os
from flask.ext.socketio import SocketIO, emit
import database as db
from jinja2 import Template
from flask import Flask, render_template, url_for, request, session;
app = Flask(__name__)

socketio = SocketIO(app)
app.secret_key = os.urandom(24).hex()
admin = False
owner = False

@socketio.on('votes')
def vote(index):
    votes = db.executeQuery("SELECT suggestion FROM suggestions INNER JOIN users ON suggestions.userid = users.userid", db.connectMaster())
    selection = votes[index]
    db.executeQuery("UPDATE suggestions SET votes = sum(votes + 1) WHERE suggestion=%s", db.connectMaster())


@socketio.on('connect')
def makeConnection():
    msgs = db.getMessages()
    names = db.getUserForMessage()
    print("Here's a message")
    i = 0
    name = db.executeQuery("SELECT username FROM suggestions INNER JOIN users ON suggestions.userid = users.userid", db.connectMaster())
    types = db.executeQuery("SELECT suggestiontype FROM suggestions INNER JOIN users ON suggestions.userid = users.userid", db.connectMaster())
    sug = db.executeQuery("SELECT suggestion FROM suggestions INNER JOIN users ON suggestions.userid = users.userid", db.connectMaster())
    vote = db.executeQuery("SELECT votes FROM suggestions INNER JOIN users ON suggestions.userid = users.userid", db.connectMaster())
    print(name)
    for tab in name:
        stuff = {'name': name[i], 'type': types[i], 'suggestion': sug[i], 'votes': vote[i]}
        i = i + 1
        sendSug(stuff)
    i = 0
    for name in names:
        tmp = {'message': msgs[i], 'user': names[i]}
        i = i + 1
        sendMessage(tmp)
    print('Yes this is connected')
    
def sendMessage(tmp):
    emit('message', tmp, broadcast=True)

def sendSug(stuff):
    print(stuff)
    emit('suggest', stuff, broadcast=True)
    
@socketio.on('test')
def testing(msg):
    print(msg)
    
@socketio.on('send')
def send(msg):
    print(msg)
    tmp = {'message': msg, 'user': session['username']}
    db.addToMessages(tmp['user'], msg)
    emit('message', tmp, broadcast=True)

@app.route('/')
def mainIndex():
    main = True
    typo = False
    other = False
    log = False
    digital = False
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname']]
    else:
        insession = False
        user = ['', '', '']
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
        user = [session['username'], session['firstname'], session['lastname'], ]
    else:
        insession = False
        user = ['', '', '']
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
        user = [session['username'], session['firstname'], session['lastname'], ]
        
            
        
            
    else:
        insession = False
        user = ['', '', '']
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
        user = [session['username'], session['firstname'], session['lastname'], ]
        
            
        
            
    else:
        insession = False
        user = ['', '', '']
    return render_template('SuggestionPage.html', tab=check, user=user, sess=insession)
    
@app.route('/suggestions/suggest')
def mainSuggestions():
    #test = url_for('thankyou')
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], ]
    else:
        insession = False
        user = ['', '', '']
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
        user = [session['username'], session['firstname'], session['lastname'], ]
        
            
        
            
    else:
        insession = False
        user = ['', '', '']
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
            db.addToUsers(request.form['firstname'], request.form['lastname'], request.form['username'], request.form['pw'], request.form['email'])
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], ]
        
            
        
            
    else:
        insession = False
        user = ['', '', '']
    return render_template('index.html', sess=insession, user=user)
    
@app.route('/login', methods=['POST'])
def mainIn():
    if request.method == 'POST':
        if db.checkexists(db.connectUsers(), request.form['username']):
            if db.matchpassword(db.connectUsers(), request.form['pw'], request.form['username']):
                session['username'] = request.form['username']
                session['firstname'] = db.executeQuery("SELECT firstname FROM users WHERE username='%s'" % (request.form['username']), db.connectUsers())
                session['lastname'] = db.executeQuery("SELECT lastname FROM users WHERE username='%s'" % (request.form['username']), db.connectUsers())
                print("Logged in")
            else:
                print("Incorrect password")
        else:
            print("Incorrect username")
            
    if 'username' in session:
        insession = True
        user = [session['username'], session['firstname'], session['lastname'], ]
        
            
        
            
    else:
        insession = False
        user = ['', '', '']
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
        user = [session['username'], session['firstname'], session['lastname'], ]
        
            
        
            
    else:
        insession = False
        user = ['', '', '']
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
        user = [session['username'], session['firstname'], session['lastname'], ]
        
            
        
            
    else:
        insession = False
        user = ['', '', '']
    return render_template('chat.html', user=user, sess=insession)

# start the server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
