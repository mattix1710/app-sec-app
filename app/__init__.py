from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import os
# from flask_sslify import SSLify

# from . import setEnv
from .async_celery import celery as celery_config

db = SQLAlchemy()
mail_service = Mail()

DB_USER = 'postgres'
DB_PASS = 'superduperpass'

# DB_CONN = 'localhost:5432'
DB_CONN = 'postgres:5432'
DB_NAME = 'droplet_db'

DB_URL = 'postgresql+psycopg://{user}:{passwd}@{url}/{db}'.format(user=DB_USER, passwd=DB_PASS, url=DB_CONN, db=DB_NAME)

# INFO: "Flask app factory pattern"
def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    
    #### session cookies ####
    # sending cookie only via HTTP
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    # sending cookie only with requests over HTTPS
    # app.config['SESSION_COOKIE_SECURE'] = True
    # https://flask.palletsprojects.com/en/2.3.x/config/#PERMANENT_SESSION_LIFETIME
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600
    
    # Flask secret key - used for signing session cookies against cookie data tampering
    app.secret_key = 'verysecretsecretkey'.encode('utf-8')

    # initializing database in the app
    db.init_app(app)

    # Initialize mail server
    app.config['SERVER_NAME'] = '127.0.0.1:5000'
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_ADDRESS')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail_service.init_app(app)
    
    # initialize Celery handler (along with connection to Redis server)
    app.config.from_mapping(
        CELERY=dict(
            broker_url = os.environ.get('REDIS_SERVER'),
            result_backend = os.environ.get('REDIS_SERVER'),
            task_ignore_result = True,
            task_track_started = True,
        ),
    )
    celery_config.celery_init_app(app)
    
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