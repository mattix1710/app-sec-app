from flask import session, redirect, url_for, request, render_template
import os

from . import auth

from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from ..models import User
from .. import db

from .helpers import hash_the_pass, server_check_session, server_set_session, SESSION_NAME, send_password_reset_email, validate_token, user_pass_update, check_admin_session, check_admin_privileges

@auth.route('/')
def index():
    return redirect(url_for('auth.register'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if server_check_session():
        return redirect(url_for('main.my_profile'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
    # if request.method == 'GET':
        
    # elif request.method == 'POST':
        user = User(email = form.email.data.lower(),
                    username = form.username.data,
                    password = hash_the_pass(form.password.data),
                    is_active = True,
                    is_admin = False)
        
        db.session.add(user)
        db.session.commit()
        server_set_session(form.username.data)
        
        return redirect(url_for('main.my_profile'))
    return render_template('auth/register.html', form=form)
        
@auth.route('/registered')
def register_done():
    return render_template('auth/register_success.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if server_check_session():
        return redirect(url_for('main.my_profile'))
    
    form = LoginForm()

    if form.validate_on_submit():
        server_set_session(form.username.data)
        return redirect(url_for('main.my_profile'))
        # return render_template('auth/login_success.html')
    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods=['POST'])
def logout():
    # pop the session data from cookie
    if SESSION_NAME in session:
        session.pop(SESSION_NAME)
    
    # DEBUG
    print("DEBUG: session cookie deleted")
    return redirect(url_for('main.home'))
  
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if server_check_session():
        return redirect(url_for('main.my_profile'))
    
    form = ForgotPasswordForm()
    
    print(os.environ.get('MAIL_PORT'))

    if form.validate_on_submit():
        print("DEBUG: submitted mail -", form.email.data)
        # INFO: using Celerys concurrency feature for unloading longer/heavy processes onto background tasks
        send_password_reset_email.delay(form.email.data)
        
        # TODO: show JS alert() and then redirect to login page
        # return redirect(url_for('auth.login'))
        
        return render_template("auth/reset_email_sent.html")

    return render_template("auth/forgot_password.html", form=form)

@auth.route('/pass-recovery', methods=['GET', 'POST'])
def set_new_password():
    if server_check_session():
        return redirect(url_for('main.my_profile'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        print("DEBUG: new password set")
        if request.args.get('token'):
            user_id = validate_token(request.args.get('token'))
            if user_id:
                user_pass_update(user_id, form.password.data)
                print("DEBUG: user data updated!")
        
        return redirect(url_for('auth.login'))
    return render_template("auth/forgot_password.html", form=form)

######################################################################
#================================ ADMIN =============================#
######################################################################
# ADMIN login
@auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if check_admin_session():
        return redirect(url_for('main.admin_panel'))
    
    form = LoginForm()
    # INFO: IDEA - add some testing if the user is requesting multiple wrong logins - prevent brute-forcing
    print("IP:", request.remote_addr)
    
    if form.validate_on_submit():
        # check if user has admin privileges
        if check_admin_privileges(form.username.data):
            server_set_session(form.username.data)
            return redirect(url_for('main.admin_panel'))
        return redirect(url_for('auth.login'))
    return render_template('auth/admin_login.html', form=form)