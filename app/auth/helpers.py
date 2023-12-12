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