from flask import session, url_for
from flask_mail import Message
from sqlalchemy import exc
import bcrypt
from datetime import datetime, timedelta
import functools
from Crypto import Random
import base64
import os

from ..models import User, Session, PassResetSession
from .. import db
from .. import mail_service

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
SESSION_TOKEN = 'save_my_bandwidth'     # TODO: change and move to env variables
TOKEN_EXPIRATION = 15*60
SERVER_IP = "127.0.0.1:5000"

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
    
def check_admin_session():
    '''
        Checks whether the session for admin exists locally.
        
        ### RETURNS:
        * True - if session exists and didn't expire yet
        * False - if session either doesn't exist, expired or user NOT admin
    '''
    try:
        if check_session():
            user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]).scalar().uid).scalar()
            if user.is_admin:
                return True
        return False
    except exc.MultipleResultsFound:
        print("AUTH_ERR: MultipleResultsFound")
        session.pop(SESSION_NAME)
        return False
    except:
        print("AUTH_ERR: not specified")
        return False

def send_password_reset_email(email):
    try:
        entry = User.query.filter_by(email=email).scalar()
        if entry == None:
            raise exc.NoResultFound
        
        token = generate_unique_token()
        # create recovery token and submit to database
        session_token = PassResetSession(
            uid = User.query.where(User.email == email).scalar().id,
            token = token,
        )
        db.session.add(session_token)
        db.session.commit()
        
        url = "http://{ip}{redirect}?token={token}".format(ip=SERVER_IP, redirect = url_for('auth.set_new_password'), token = token)
        
        msg = Message(subject='Password reset for your account', sender = os.environ.get('MAIL_ADDRESS'), recipients=[entry.email])
        msg.html = "Hello fellow blood donor!</br>You have requested a password reset for your Kropelka Account.</br>"\
            "Please follow this link to reset your password: <a href='{password_reset_url}'>Click</a>.</br>"\
            "If you cannot click on provided link, please copy and paste this link to your browser search bar and proceed:</br>"\
            "{password_reset_url}</br>"\
            "This link will be active for the next {token_expiration} minutes.</br>"\
            "If you did not request a password reset, please change your password as soon as possible!"\
            .format(password_reset_url = url, token_expiration = int(TOKEN_EXPIRATION/60))
        mail_service.send(msg)
    except exc.MultipleResultsFound:
        print("DEBUG: e-mail not sent: Too many results!")
    except exc.NoResultFound:
        # INFO: for further development - if this exception occurs, it means the user typed wrong e-mail address
        print("DEBUG: e-mail not sent: No results found!")
    except:
        print("DEBUG: Noooooo, God please, no!")
    
def __generate_reset_token(in_bytes = False):
    '''
        Generates reset/recovery token for forgotten password functionality
        
        :param in_bytes: sets output format to bytes
    '''
    rand_bytes = Random.get_random_bytes(50)
    bytes_base = base64.urlsafe_b64encode(rand_bytes)
    
    if in_bytes:
        return bytes_base[:50]
    return bytes_base[:50].decode('utf-8')

def generate_unique_token():
    '''
        Generates unique reset/recovery token for forgotten password functionality
        
        Uses generate_reset_token() method
    '''
    tokens = PassResetSession.query.all()
    if_token_exists = False
    
    while(True):
        token = __generate_reset_token()
        for el in tokens:
            if el.token_matches(token):
                if_token_exists = True
                break
        if if_token_exists:
            continue
        break
    return token
    

def validate_token(token):
    '''
        Validates reset/recovery token integrity
        
        :param token: password reset token provided for the user
        
        RETURNS
        * ID of a User - if matching record was found in the database
        * None - if no matching record found
    '''
    try:
        entry = PassResetSession.query.filter_by(token = token).scalar()
        # if there is no such entry
        if entry == None:
            raise exc.NoResultFound
        # if current token has already expired        
        if datetime.now() > entry.timestamp + timedelta(0, TOKEN_EXPIRATION):
            raise ValueError
        
        return entry.uid
    except exc.NoResultFound:
        print("DEBUG: No matching password reset token entry!")
    except ValueError:
        print("DEBUG: Token has already expired!")
    except:
        return None
    
def user_pass_update(id, password):
    user = User.query.where(User.id == id).scalar()
    pass_hash = hash_the_pass(password)
    user.password = pass_hash
    # db.session.add(user)
    db.session.commit()