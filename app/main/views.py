from flask import render_template, redirect, url_for, request, session
from datetime import datetime, timedelta
from . import main

from .. import db
from ..models import Photo, User, Session

from ..auth.helpers import server_set_session, server_check_session, SESSION_NAME

@main.route('/')
def home():
    
    # session['my_data'] = "Hello you!"
    
    if 'code' in request.args:
        print(request.args['code'])
    # return render_template("")
    
    user_agent_data = request.headers.get('User-Agent')
    my_ip = request.headers
    
    return "<h1>Main page</h1><p>{UA}</p><p>{IP}</ip>".format(UA=user_agent_data, IP=my_ip)    # return a string

@main.route('/my_profile', methods=['GET', '[POST]'])
def my_profile():
    # if user is logged in - show its profile data
    if server_check_session():        
        user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]['id']).scalar().uid).scalar()      
        return render_template('profile.html', user = user)
    # otherwise - redirect to login page
    return redirect(url_for('auth.login'))