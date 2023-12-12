from flask import session
import bcrypt
from datetime import datetime, timedelta

from ..models import User, Session
from .. import db

def hash_the_pass(passwd):
    passwd = passwd.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(passwd, salt)
    
    # returning the hash in decoded version from bytes to string
    return hashed_pw.decode('utf-8')

#############################################
# TIME DELTA SECONDS
DELTA_SECS = 3600

def check_session():
    '''
        Checks whether the session is ok or wrong
    '''
    if 'session' in session:
        session_data = Session.query.where(Session.id == session['session']).scalar()
        # if session with this ID exists
        if session_data != None:
            # if session didn't expire
            if session_data.timestamp + timedelta(0, DELTA_SECS) > datetime.now():
                return True
    # otherwise - pop the data from cookie and return False
    session.pop('session')
    return False

def set_session(login):
    '''
        Sets new session based on given credentials
    '''
    new_session = Session(uid = User.query.where(User.username == login).scalar().id)
    db.session.add(new_session)
    
    session['session'] = Session(uid = User.query.where(User.username == login).scalar().id).id
    
    db.session.commit()