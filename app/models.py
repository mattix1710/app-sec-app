# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

from . import db

# model class created ONLY for testing purposes
# TODO: delete before finishing the project
class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    src = db.Column(db.String(100), nullable=False)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(72), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    # INFO: only for DEBUG purposes
    def get_user_data(self):
        print("User - {}\nemail: {}\npass_hash: {}".format(username, email, password))