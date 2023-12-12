from flask import render_template, redirect, url_for, request, session
from datetime import datetime, timedelta
from . import main

from .. import db
from ..models import Photo, User, Session

from ..auth.helpers import check_session

@main.route('/')
def home():
    
    session['my_data'] = "Hello you!"
    
    if 'code' in request.args:
        print(request.args['code'])
    # return render_template("")
    
    user_agent_data = request.headers.get('User-Agent')
    my_ip = request.headers
    
    return "<h1>Main page</h1><p>{UA}</p><p>{IP}</ip>".format(UA=user_agent_data, IP=my_ip)    # return a string

@main.route('/my_profile', methods=['GET', '[POST]'])
def my_profile():
    # check if session exists - if yes, list user data
    # SQL:
    #   SELECT * FROM users WHERE id = (SELECT uid FROM sessions WHERE id = 'FFA582B309ACD115');
    # session_uid = db.session.query(Session.uid).filter(Session.id == 'FFA582B309ACD115').scalar()
    
    # user = db.session.query(User).filter(User.id == session_uid).all()
    
    # session_time = db.session.query(Session.timestamp).where(Session.id == 'FFA582B309ACD115').scalar()
    
    # print(User.query.where(User.username == 'mattix').scalar().email)
    
    # INFO: creating new user and adding new session
    user = User(
        email = "super@email.com",
        username = "user_buster",
        password = "hush_hush_baby",
        is_active = True)
    
    db.session.add(user)
    db.session.add(Session(uid = User.query.where(User.email == "super@email.com").scalar().id))
        
    db.session.commit()
    
    sess = Session.query.where(Session.uid == User.query.where(User.email == "super@email.com").scalar().id).scalar().id
    
    # datetime.now()
    # ss_time = datetime.strptime(session_time, )
    # timedelta(0, 7200)
    # print(session_time + timedelta(0, 7200))
    
    
    if request.form:
        print("SOMETHING CHANGED")
    return render_template('profile.html', session_id = sess)