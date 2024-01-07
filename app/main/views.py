from flask import render_template, redirect, url_for, request, session
from . import main

from .. import db
from ..models import User, Session, PassResetSession

from ..auth.helpers import server_set_session, server_check_session, SESSION_NAME, check_admin_session
from .helpers import *

@main.route('/')
def home():
    return render_template('main.html', user_session=server_check_session(), blood_list=gather_blood_type_stats())

@main.route('/my_profile', methods=['GET', '[POST]'])
def my_profile():
    # if user is logged in - show its profile data
    if server_check_session():        
        user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]['id']).scalar().uid).scalar()      
        return render_template('profile.html', user = user, user_session = True)
    # otherwise - redirect to login page
    return redirect(url_for('auth.login'))

@main.route('/admin_tools/admin_panel')
def admin_panel():
    if check_admin_session():
        reset_sessions = PassResetSession.query.all()
        user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]['id']).scalar().uid).scalar()
        return render_template('admin/main_panel.html', user = user, user_session = True, table = reset_sessions, model = PassResetSession)
    return redirect(url_for('main.home'))

# INFO: temporary site - created for checking celery proper installation
@main.route("/really_long_task")
def long_task():
    really_long_wait.delay()
    return render_template('base.html')

@main.route("/tests")
def tests():
    gather_blood_type_stats()
    return "<h1>Tests is progress</h1>"