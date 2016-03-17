# for console printing purposes
from __future__ import print_function # In python 2.7
import sys

from flask import (render_template, 
				   make_response,
				   jsonify, 
				   send_from_directory, 
                   flash, 
                   redirect,
                   session, 
                   url_for, 
                   request, 
                   g,
                   abort )
from flask.ext.login import (login_user, 
                             logout_user, 
                             current_user,
                             login_required )
from app import app, db, lm
from .forms import get_swtIDForm, MyForm, LoginForm, InputURLform
from .models import User
import requests
import urllib2
import lxml.html
import StringIO


# for debugging purposes by SaiGo
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('+++++++++++++++++++++++ Starting log message ++++++++++++++.') 

@app.before_request
def get_current_user():
    g.user = None
    email = session.get('email')
    if email is not None:
        g.user = email

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def home_page():
    logging.debug('/index GET')
    form = InputURLform(request.form)

    # this is activated when the form is filled POSTed by user
    if form.validate_on_submit():
       logging.debug('/indexPOST')
       entered_url = form.url.data
       logging.debug(entered_url)
    
       return render_template('showPg.html', 
                           title='input URL POST',
                           url=entered_url)

    # this is activated for the first round
    return render_template('inputURLform.html',
                            title='input URL GET',
                            form=form)
#-----------------------------------------------

@app.route('/showPg')
def showURL_page():
    logging.debug('/showPg')
    entered_url = form.url.data
    return render_template('showPg.html', 
                           url=entered_url)

@app.route('/_auth/login', methods=['GET', 'POST'])
def login_handler():
    """This is used by the persona.js file to kick off the
    verification securely from the server side.  If all is okay
    the email address is remembered on the server.
    """
    resp = requests.post(app.config['PERSONA_VERIFIER'], data={
        'assertion': request.form['assertion'],
        'audience': request.host_url,
    }, verify=True)
    if resp.ok:
        verification_data = resp.json()
        if verification_data['status'] == 'okay':
            session['email'] = verification_data['email']
            return 'OK'
    abort(400)

@app.route('/_auth/logout', methods=['POST'])
def logout_handler():
    """This is what persona.js will call to sign the user
    out again.
    """
    session.clear()
    return 'OK'

@app.route('/get_swtID', methods=['GET', 'POST'])
def get_swtID():
    form = get_swtIDForm()
    return render_template('get_swtID.html',
                           title='Sign In',
                           form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       login_user(user)
       flask.flash('logged in successfully')
       
       next = flask.request.args.get('next')
       if not next_is_valid(next):
          return flask.abort(400)
          
       return flask.redirect(next or flask.url_for('/index'))
    return render_template('login.html', form=form)

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)

@lm.user_loader
def load_user(id):
    # user Id from Flask-Login is unicode, thats why we need to convert
    # to int before sending it to database (SQLAlchemy) pkg
    return User.query.get(int(id))  

if __name__ == '__main__':
    app.run()
