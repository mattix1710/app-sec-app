from flask import render_template, redirect, url_for, request
from . import main

@main.route('/')
def home():
    return "<h1>Main page</h1>"    # return a string

