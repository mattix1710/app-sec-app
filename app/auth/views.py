from flask import Flask, session, redirect, url_for, request, render_template
import cgi
import re

from . import auth

from .forms import RegistrationForm, LoginForm
from ..models import User, Session
from .. import db

from .helpers import hash_the_pass, server_check_session, server_set_session

@auth.route('/')
def index():
    return redirect(url_for('auth.register'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if server_check_session():
        return redirect(url_for('main.my_profile'))
    
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
        server_set_session(form.username.data)
        
        return redirect(url_for('main.my_profile'))
    return render_template('auth/register.html', form=form)
        
@auth.route('/registered')
def register_done():
    return render_template('auth/register_success.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if server_check_session():
        return redirect(url_for('main.my_profile'))
    
    form = LoginForm()

    if form.validate_on_submit():
        server_set_session(form.username.data)
        return redirect(url_for('main.my_profile'))
        # return render_template('auth/login_success.html')
    return render_template('auth/login.html', form=form)