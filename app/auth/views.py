from flask import render_template, redirect, url_for, request
from . import auth
from .. import db
from ..models import users
import cgi
import re
import bcrypt
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
'''

def sanitise(input):
    tst = re.findall('^[A-Za-z]\\w*$', input)
    # tst = None if len(tst) <= 0 else tst[0]
    return tst[0]

def check_user(username, password):
    pswd = password.encode('utf-8')
    entry = db.session.query(users).filter(users.username == username)
    if entry.count() > 1 or entry.count() <= 0:
        raise IndexError
    hashed = entry[0].password.strip().encode('utf-8')
    if not bcrypt.checkpw(pswd, hashed):
        raise InterruptedError
    cookie = "ahahahah"
    return cookie

@auth.route('/')
def index():
    return redirect(url_for('auth.register'))

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        try:
            sane = sanitise(request.form['username'])
            # if not sane:
            #    return render_template('login.html', error=True)
            check_user(sane, request.form['password'])
            return render_template('success.html')
            # TODO add redirect to user page
            #return redirect(url_for('main.home'))
        except:
            return render_template('login.html', error=True)