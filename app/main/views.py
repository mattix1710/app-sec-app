from flask import render_template, redirect, url_for, request
from . import main

from .. import db
from ..models import Photo

@main.route('/')
def home():
    return "<h1>Main page</h1>"    # return a string

# route created ONLY for testing purposes
# TODO: delete before finishing the project
@main.route('/photos')
def photo_display():
    photos = db.session.query(Photo).all()
    print(photos[0].name)
    return render_template('photos.html', photos=photos)