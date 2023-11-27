# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

from . import db

class users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(72), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

# model class created ONLY for testing purposes
# TODO: delete before finishing the project
class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    src = db.Column(db.String(100), nullable=False)
