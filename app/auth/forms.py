from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
import bcrypt

from ..models import User, Post
from ..main.helpers import process_title

class RegistrationForm(FlaskForm):
    email = StringField('e-mail', validators=[DataRequired(), Length(1, 100), Email()])
    
    username = StringField('Username', validators=[DataRequired(), Length(1, 50), Regexp('^[A-Za-z]\\w*$')])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password too short."), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('E-mail already registered!')
        
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 50), Regexp('^[A-Za-z]\\w*$')])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log-In')

    def validate_username(self, field):
        pswd = self.password.data.encode('utf-8')
        entry = User.query.filter_by(username=self.username.data)

        if entry.count() > 1 or entry.count() <= 0:
            raise ValidationError('Wrong Username/Password')
        hashed = entry[0].password.strip().encode('utf-8')
        if not bcrypt.checkpw(pswd, hashed):
            raise ValidationError('Wrong Username/Password')


class ForgotPasswordForm(FlaskForm):
    email = StringField('e-mail', validators=[DataRequired(), Length(1, 100), Email()])

    submit = SubmitField('Confirm')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password too short."), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    submit = SubmitField('Change password')


class CreatePostForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', render_kw={"rows": 40, "cols": 100}, validators=[DataRequired()])

    submit = SubmitField('Save post')

    def validate_title(self, field):
        title_normalised = process_title(field.data)
        print(process_title(field.data))
        if Post.query.where(Post.title_normalized == title_normalised).count() > 0:
            raise ValidationError('Post Exists')


class EditPostForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', render_kw={"rows": 40, "cols": 100}, validators=[DataRequired()])

    submit = SubmitField('Save post')

    def validate_title(self, field):
        title_normalised = process_title(field.data)
        print(process_title(field.data))
        if Post.query.where(Post.title_normalized == title_normalised).count() > 1:
            raise ValidationError('Post Exists')


class AddCommentForm(FlaskForm):
    content = TextAreaField('Comment body', render_kw={"rows": 4, "cols": 50}, validators=[DataRequired()])

    submit = SubmitField('Post comment')