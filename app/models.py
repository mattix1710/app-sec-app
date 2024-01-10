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
    is_supervisor = db.Column(db.Boolean, server_default=db.FetchedValue())
    is_admin = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    last_logged = db.Column(db.Date, nullable=False, server_default=db.FetchedValue())

    # INFO: only for DEBUG purposes
    def get_user_data(self):
        print("User - {}\nemail: {}\npass_hash: {}".format(self.username, self.email, self.password))
        
    def get_headers(self):
        return ['id', 'username', 'email', 'is_active', 'is_supervisor', 'is_admin']
        
class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Uuid, primary_key=True, server_default=db.FetchedValue())
    uid = db.Column(db.ForeignKey('users.id'), nullable=False, server_default=db.FetchedValue())
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    user = db.relationship('User', primaryjoin='Session.uid == User.id', backref='sessions')
    
class PassResetSession(db.Model):
    __tablename__ = 'pass_reset_session'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    uid = db.Column(db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, server_default=db.FetchedValue())
    token = db.Column(db.String(50), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    user = db.relationship('User', primaryjoin='PassResetSession.uid == User.id', backref='pass_reset_sessions')

    def token_matches(self, new_token):
        if self.token == new_token:
            return True
        return False
    
    def get_headers(self):
        return ['id', 'uid', 'token', 'timestamp']
    
class BloodState(db.Model):
    __tablename__ = 'blood_state'

    id = db.Column(db.SmallInteger, primary_key=True, server_default=db.FetchedValue())
    blood_type = db.Column(db.String(7), nullable=False, unique=True)
    amount = db.Column(db.String(3), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    
class Branch(db.Model):
    __tablename__ = 'branch'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    supervisor = db.Column(db.ForeignKey('users.id'), nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False, unique=True)

    user = db.relationship('User', primaryjoin='Branch.supervisor == User.id', backref='branches')
    
    def get_headers_details(self):
        return ['supervisor', 'name', 'address']

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    branch_id = db.Column(db.ForeignKey('branch.id', ondelete='CASCADE'), nullable=False, server_default=db.FetchedValue())
    title = db.Column(db.Text, nullable=False, unique=True)
    title_normalized = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)

    branch = db.relationship('Branch', primaryjoin='Post.branch_id == Branch.id', backref='posts')
    
class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    post_id = db.Column(db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False, server_default=db.FetchedValue())
    author_id = db.Column(db.ForeignKey('users.id'), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.Text, nullable=False)

    author = db.relationship('User', primaryjoin='Comment.author_id == User.id', backref='comments')
    post = db.relationship('Post', primaryjoin='Comment.post_id == Post.id', backref='comments')