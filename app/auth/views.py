from flask import Flask, session, redirect, url_for, request, render_template
import bcrypt
import cgi
import re

from . import auth

from .forms import RegistrationForm
from ..models import User
from .. import db

class TooManyUsersError(Exception):
    # Raise this when database query gets 0 or more users when
    # it's supposed to get only one
    pass

class InvalidPassHashError(Exception):
    # Raise this if password hash does not match
    pass

def hash_the_pass(passwd):
    passwd = passwd.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(passwd, salt)
    
    # returning the hash in decoded version from bytes to string
    return hashed_pw.decode('utf-8')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
    # if request.method == 'GET':
        
    # elif request.method == 'POST':
        user = User(email = form.email.data.lower(),
                    username = form.username.data,
                    password = hash_the_pass(form.password.data),
                    is_active = True,
                    is_admin = False)
        
        db.session.add(user)
        db.session.commit()
        
        
        ''' cannot use after adding to database and commiting (the data is flushed from memory (?))
            AND the error occurs:
            sqlalchemy.orm.exc.DetachedInstanceError: Instance <User at 0x21bb9c9ed50> is not bound to a Session; attribute refresh operation cannot proceed (Background on this error at: https://sqlalche.me/e/20/bhk3) '''
        # user.get_user_data()
        
        return redirect(url_for('auth.register_done'))
    
    return render_template('auth/register.html', form=form)
        
@auth.route('/registered')
def register_done():
    return render_template('auth/register_success.html')

'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
'''

def sanitise(input):
    tst = re.findall('^[A-Za-z]\\w*$', input)
    return tst[0]

def check_user(username, password):
    pswd = password.encode('utf-8')
    entry = db.session.query(User).filter(User.username == username)

    if entry.count() > 1 or entry.count() <= 0:
        raise TooManyUsersError
    hashed = entry[0].password.strip().encode('utf-8')
    if not bcrypt.checkpw(pswd, hashed):
        raise InvalidPassHashError
    
    # TODO Session biscuit
    cookie = "ahahahah"
    return cookie

@auth.route('/')
def index():
    return redirect(url_for('auth.register'))

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
        try:
            sane = sanitise(request.form['username'])
            check_user(sane, request.form['password'])
            return render_template('auth/login_success.html')
            # TODO add redirect to user page
            #return redirect(url_for('main.home'))
        except:
            return render_template('auth/login.html', error=True)