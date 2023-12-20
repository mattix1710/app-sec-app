from flask import render_template, redirect, url_for, request, session
from datetime import datetime, timedelta
from . import main

from .. import db
from ..models import User, Session

from ..auth.helpers import server_set_session, server_check_session, SESSION_NAME

@main.route('/')
def home():
    return render_template('main.html', user_session=server_check_session())

@main.route('/my_profile', methods=['GET', '[POST]'])
def my_profile():
    # if user is logged in - show its profile data
    if server_check_session():        
        user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]['id']).scalar().uid).scalar()      
        return render_template('profile.html', user = user, user_session=True)
    # otherwise - redirect to login page
    return redirect(url_for('auth.login'))