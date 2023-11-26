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
