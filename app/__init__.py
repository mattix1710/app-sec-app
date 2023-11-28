from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
# session = Session()

DB_USER = 'postgres'
DB_PASS = 'superduperpass'

DB_CONN = 'localhost:5432'
# DB_NAME = 'photo_browser'     # TODO: delete before finishing
DB_NAME = 'droplet_db'

DB_URL = 'postgresql+psycopg://{user}:{passwd}@{url}/{db}'.format(user=DB_USER, passwd=DB_PASS, url=DB_CONN, db=DB_NAME)

SESSION_TYPE = 'sqlalchemy'

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.secret_key = 'verysecretsecretkey'.encode('utf-8')

    # initializing database in the app
    db.init_app(app)
    
    Bootstrap(app)
    
    # initialize session in the app
    # session.init_app(app)
    
    ############################################
    # import app blueprints (auth, api, etc.)
    
    # registering MAIN blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # registering AUTH blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # registering API blueprint
    
    # TODO: create API - for now leave it commented
    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/')
    
    return app