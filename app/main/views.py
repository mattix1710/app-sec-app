from flask import render_template, redirect, url_for, request, session
from . import main

from .. import db
from ..models import User, Session, PassResetSession

from ..auth.helpers import server_set_session, server_check_session, SESSION_NAME, check_admin_session, check_session, get_supervisor_branch
from ..auth.helpers import get_post, get_posts, create_post, update_post, delete_post, get_post_comments, add_comment
from .helpers import *

from ..auth.forms import CreatePostForm, EditPostForm, AddCommentForm


@main.route('/', methods=['GET', 'POST'])
def home():
    user_session, user_supervisor = check_session()
    
    return render_template('main.html', 
                           is_supervisor=user_supervisor, user_session=user_session, blood_list=gather_blood_type_stats())

@main.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    # if user is logged in - show its profile data
    user_session, user_supervisor = check_session()
    if user_session:
        user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]['id']).scalar().uid).scalar()      
        return render_template('profile.html', user = user, user_session = True, is_supervisor = user_supervisor)
    # otherwise - redirect to login page
    return redirect(url_for('auth.login'))

@main.route('/admin_tools/admin_panel')
def admin_panel():
    print(session[SESSION_NAME])
    if check_admin_session():
        user_list = User.query.all()
        print(user_list)
        
        reset_sessions = PassResetSession.query.all()
        user = User.query.where(User.id == Session.query.where(Session.id == session[SESSION_NAME]['id']).scalar().uid).scalar()
        return render_template('admin/main_panel.html', user = user, user_session = True, table = reset_sessions, model = PassResetSession, user_table = user_list)
    return redirect(url_for('main.home'))

@main.route("/news/<post_title>", methods=['GET', 'POST'])
def news_details(post_title=None):
    if post_title == None:
        return redirect(url_for('main.home'))
    user_session, user_supervisor = check_session()
    try:    
        post = get_post(post_title)
        comments = get_post_comments(post_title)
    except:
        return redirect(url_for('main.home'))
    form = AddCommentForm()

    if form.validate_on_submit():
        add_comment(post_title, form)
        return redirect(url_for('main.news_details', post_title=post_title))

    return render_template('news.html', post = post, comments = comments, form = form,
                            is_supervisor = user_supervisor, user_session = user_session)
    
@main.route("/branch")
def branch_desc():
    user_session, user_supervisor = check_session()
    
    if user_supervisor:
        branch_data = get_supervisor_branch()
        print(branch_data)
        posts = get_posts()
        return render_template('branch/branch-details.html', branch = branch_data, user_session = True, is_supervisor = user_supervisor, posts = posts)
    return redirect(url_for('main.home'))

@main.route("/branch/create", methods=['GET', 'POST'])
def branch_create_post():
    user_session, user_supervisor = check_session()

    if user_supervisor:
        branch_data = get_supervisor_branch()
        form = CreatePostForm()

        if form.validate_on_submit():
            create_post(form.title.data, form.content.data)
            return redirect(url_for('main.branch_desc'))

        return render_template('branch/create-post.html', branch=branch_data, form=form, is_supervisor = user_supervisor, user_session = user_session)
    return redirect(url_for('main.home'))

@main.route("/branch/edit/<post_title>", methods=['GET', 'POST'])
def branch_edit_post(post_title):
    user_session, user_supervisor = check_session()

    if user_supervisor:
        branch_data = get_supervisor_branch()

        try:
            post = get_post(post_title)
        except:
            return redirect(url_for('main.branch_desc'))
        
        if post.branch_id == branch_data.supervisor:
            form = EditPostForm(obj=post)

            if form.validate_on_submit():
                update_post(branch_data.supervisor, post_title, form)
                return redirect(url_for('main.branch_desc')) 

            return render_template('branch/create-post.html', branch=branch_data, form=form, is_supervisor = user_supervisor, user_session = user_session)
        return redirect(url_for('main.branch_desc'))
    return redirect(url_for('main.home'))

@main.route("/branch/delete/<post_title>", methods=['GET', 'POST'])
def branch_delete_post(post_title):
    user_session, user_supervisor = check_session()

    if user_supervisor:
        branch_data = get_supervisor_branch()
        try:
            post = get_post(post_title)
            if post.branch_id == branch_data.supervisor:
                delete_post(post)
        except:
            return redirect(url_for('main.branch_desc'))
        return redirect(url_for('main.branch_desc'))
    return redirect(url_for('main.home'))