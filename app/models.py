# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(72), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    last_logged = db.Column(db.Date, nullable=False, server_default=db.FetchedValue())

    # INFO: only for DEBUG purposes
    def get_user_data(self):
        print("User - {}\nemail: {}\npass_hash: {}".format(self.username, self.email, self.password))
        
class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Uuid, primary_key=True, server_default=db.FetchedValue())
    uid = db.Column(db.ForeignKey('users.id'), nullable=False, server_default=db.FetchedValue())
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    user = db.relationship('User', primaryjoin='Session.uid == User.id', backref='sessions')