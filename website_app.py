from app import create_app
from celery import Celery

flask_app = create_app()
celery_app = flask_app.extensions['celery']