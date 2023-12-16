from flask import session
from flask_mail import Message
import bcrypt
from datetime import datetime, timedelta
import functools
from Crypto import Random
import base64

from ..models import User, Session
from .. import db
from .. import mail

def hash_the_pass(passwd):
    passwd = passwd.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(passwd, salt)
    
    # returning the hash in decoded version from bytes to string
    return hashed_pw.decode('utf-8')

#############################################
# TIME DELTA SECONDS
DELTA_SECS = 3600

SESSION_NAME = 'session_data'

SESSION_TOKEN = 'save_my_bandwidth'

def check_session():
    '''
        Checks whether the session exists locally.
        
        ### RETURNS:
        * True - if session exists and didn't expire yet
        * False - if session either doesn't exist or expired
    '''
    if SESSION_NAME in session:
        session_data = Session.query.where(Session.id == session[SESSION_NAME]).scalar()
        # if session with this ID exists
        if session_data != None:
            # if session didn't expire
            if session_data.timestamp + timedelta(0, DELTA_SECS) > datetime.now():
                return True
            # otherwise - pop the data from cookie and return False
            session.pop(SESSION_NAME)
    return False

def set_session(login):
    '''
        Sets new session based on given credentials
    '''
    new_session = Session(uid = User.query.where(User.username == login).scalar().id)
    db.session.add(new_session)
    db.session.commit()

    session[SESSION_NAME] = str(new_session.id)
    
def server_check_session():
    '''
        Checks whether the session exists locally.
        Similar to 'check_session()' method, but evaluates the data stored in the cookie,
        skipping the check on the database side.
        
        ### RETURNS:
        * True - if session exists and didn't expire yet
        * False - if session either doesn't exist or expired
    '''
    
    if SESSION_NAME in session:
        token = (str(session[SESSION_NAME]['id']) + str(session[SESSION_NAME]['timestamp']) + str(SESSION_TOKEN)).encode('utf-8')
        # if session token matches
        if bcrypt.checkpw(token, session[SESSION_NAME]['token']):
            # if session didn't expire
            if datetime.fromtimestamp(session[SESSION_NAME]['timestamp']) + timedelta(0, DELTA_SECS) > datetime.now():
                return True
            # otherwise - pop the data from cookie and return False
            session.pop(SESSION_NAME)
    return False    
    
def server_set_session(login):
    '''
        Sets new session based on given credentials.
        Similar to 'set_session()' method, but prepares the data on the server side (adds session token for server verification)
        
    '''
    if SESSION_NAME in session:
        session.pop(SESSION_NAME)
    
    new_session = Session(uid = User.query.where(User.username == login).scalar().id)
    db.session.add(new_session)
    db.session.commit()

    salt = bcrypt.gensalt()
    
    token = (str(new_session.id) + str(new_session.timestamp.timestamp()) + str(SESSION_TOKEN)).encode('utf-8')
    
    session[SESSION_NAME] = {
        "id": str(new_session.id),
        "timestamp": new_session.timestamp.timestamp(),
        "token": bcrypt.hashpw(token, salt)
    }

def send_password_reset_email(email):
    entry = User.query.filter_by(email=email)
    if entry.count() == 1:
        # Send email
        msg = Message(subject='You requested a password reset', sender='a.dam.krew@hotmail.com', recipients=[entry[0].email])
        msg.html = "Hi there,\nyou requested a password reset for you Kropelka Account.</br>Please follow this link to reset your password <a href='www.google.com'>reset password</a>."
        msg.html += "</br>If you did not request a password reset, please change your password as soon as possible!"
        # DEBUG
        print('DEBUG: password-reset: sending message...')
        mail.send(msg)
        # DEBUG
        print('DEBUG: password-reset message sent')
    print('no')
    
def generate_reset_token(in_bytes = False):
    rand_bytes = Random.get_random_bytes(50)
    bytes_base = base64.urlsafe_b64encode(rand_bytes)
    
    if in_bytes:
        return bytes_base[:50]
    return bytes_base[:50].decode('utf-8')