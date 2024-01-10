from flask import render_template, redirect, url_for, request, session
from . import main

from .. import db
from ..models import User, Session, PassResetSession

from ..auth.helpers import server_set_session, server_check_session, SESSION_NAME, check_admin_session, check_session, get_supervisor_branch
from .helpers import *


@main.route('/', methods=['GET', 'POST'])
def home():
    user_session, user_supervisor = check_session()
    
    return render_template('main.html', 
                           is_supervisor=user_supervisor, user_session=user_session, blood_list=gather_blood_type_stats())

@main.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    # if user is logged in - show its profile data
    user_session, user_supervisor = check_session()
    if user_session:
        user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]['id']).scalar().uid).scalar()      
        return render_template('profile.html', user = user, user_session = True, is_supervisor = user_supervisor)
    # otherwise - redirect to login page
    return redirect(url_for('auth.login'))

@main.route('/admin_tools/admin_panel')
def admin_panel():
    print(session[SESSION_NAME])
    if check_admin_session():
        user_list = User.query.all()
        print(user_list)
        
        reset_sessions = PassResetSession.query.all()
        user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]['id']).scalar().uid).scalar()
        return render_template('admin/main_panel.html', user = user, user_session = True, table = reset_sessions, model = PassResetSession, user_table = user_list)
    return redirect(url_for('main.home'))

@main.route("/news/<post_title>", methods=['GET', 'POST'])
def news_details(post_title=None):
    if post_title == None:
        return redirect(url_for('main.home'))
    
@main.route("/branch")
def branch_desc():
    user_session, user_supervisor = check_session()
    
    if user_supervisor:
        branch_data = get_supervisor_branch()
        print(branch_data)
        return render_template('branch/branch-details.html', branch = branch_data, user_session = True, is_supervisor = user_supervisor)
    return redirect(url_for('main.home'))