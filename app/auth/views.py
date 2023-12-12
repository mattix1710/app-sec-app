from flask import Flask, session, redirect, url_for, request, render_template
import cgi
import re

from . import auth

from .forms import RegistrationForm, LoginForm
from ..models import User, Session
from .. import db

from .helpers import hash_the_pass

@auth.route('/')
def index():
    return redirect(url_for('auth.register'))

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
        
        db.session.add(Session(uid = User.query.where(User.email == form.email.data.lower()).scalar().id))
        
        db.session.commit()
        
        session['session'] = Session.query.where(Session.uid == User.query.where(User.email == form.email.data.lower()).scalar().id).order_by(Session.timestamp).limit(1).scalar()
        
        ''' cannot use after adding to database and commiting (the data is flushed from memory (?))
            AND the error occurs:
            sqlalchemy.orm.exc.DetachedInstanceError: Instance <User at 0x21bb9c9ed50> is not bound to a Session; attribute refresh operation cannot proceed (Background on this error at: https://sqlalche.me/e/20/bhk3) '''
        # user.get_user_data()
        
        return redirect(url_for('auth.register_done'))
    
    # TODO: go to /my_profile
    return render_template('auth/register.html', form=form)
        
@auth.route('/registered')
def register_done():
    return render_template('auth/register_success.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # TODO set session token

        return render_template('auth/login_success.html')
        # TODO add redirect to user page
        #return redirect(url_for('main.home'))

    return render_template('auth/login.html', form=form)