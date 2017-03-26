import os
import database as db
from jinja2 import Template
from flask import Flask, render_template, url_for, request;
app = Flask(__name__)

@app.route('/')
def mainIndex():
    mainLink = url_for('mainIndex')
    photoLink = url_for('mainTypo')
    aboutLink = url_for('mainAbout')
    suggestLink = url_for('mainSuggest')
    #print(photoLink)
    return render_template('index.html', link1=photoLink, link2=mainLink, link3=aboutLink, link4=suggestLink, link20=test)

@app.route('/typography')
def mainTypo():
    typoLib = [{'file':'Image01.jpeg',
    'title': '13 Years Old'},
    {'file':'Image02.jpeg',
    'title': 'Triggered'},
    {'file': 'Image03.jpeg',
    'title': 'Comment Below'},
    {'file': 'Image04.jpeg',
    'title': 'Rule 71'}]
    mainLink = url_for('mainIndex')
    photoLink = url_for('mainTypo')
    aboutLink = url_for('mainAbout')
    suggestLink = url_for('mainSuggest')
    return render_template('page2.html', link1=photoLink, link2=mainLink, images=typoLib, link3=aboutLink, link4=suggestLink)
    
@app.route('/about')
def mainAbout():
    selfie = "selfie.jpeg"
    alias = True
    mainLink = url_for('mainIndex')
    photoLink = url_for('mainTypo')
    aboutLink = url_for('mainAbout')
    suggestLink = url_for('mainSuggest')
    return render_template('page3.html', link1=photoLink, link2=mainLink, image=selfie, link3=aboutLink, link4=suggestLink, name=alias)
    
@app.route('/suggestions')
def mainSuggest():
    check = db.executeQuery("SELECT * FROM suggestions", db.connectSugg())
    linkSugg = url_for('mainSuggestions')
    mainLink = url_for('mainIndex')
    photoLink = url_for('mainTypo')
    aboutLink = url_for('mainAbout')
    suggestLink = url_for('mainSuggest')
    return render_template('SuggestionPage.html', link5=linkSugg, link1=photoLink, link2=mainLink, link3=aboutLink, link4=suggestLink, tab=check)
    
@app.route('/suggestions/suggest')
def mainSuggestions():
    suggestLink = url_for('mainSuggest')
    mainLink = url_for('mainIndex')
    photoLink = url_for('mainTypo')
    aboutLink = url_for('mainAbout')
    #test = url_for('thankyou')
    return render_template('suggestion.html', link1=photoLink, link2=mainLink, link3=aboutLink, link4=suggestLink)
    
@app.route('/thankyou', methods=['POST'])
def test():
    fname = request.form['firstname']
    lname = request.form['lastname']
    age = request.form['age']
    sugty = request.form['sugtype']
    sug = request.form['sug']
    db.addToSuggestions(fname, lname, age, sugty, sug)
    mainLink = url_for('mainIndex')
    photoLink = url_for('mainTypo')
    aboutLink = url_for('mainAbout')
    suggestLink = url_for('mainSuggest')
    return render_template('thankyou.html', link1=photoLink, link2=mainLink, link3=aboutLink, link4=suggestLink)

# start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
