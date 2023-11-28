from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DB_USER = 'appsec'
DB_PASS = 'superduperpass'

DB_CONN = 'localhost:5432'
DB_NAME = 'photo_browser'

DB_URL = 'postgresql+psycopg://{user}:{passwd}@{url}/{db}'.format(user=DB_USER, passwd=DB_PASS, url=DB_CONN, db=DB_NAME)

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

    # initializing database in the app
    db.init_app(app)
    
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