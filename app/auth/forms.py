from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
import bcrypt

from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('e-mail', validators=[DataRequired(), Length(1, 100), Email()])
    
    username = StringField('Username', validators=[DataRequired(), Length(1, 50), Regexp('^[A-Za-z]\\w*$')])
    
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
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

    submit = SubmitField('Forgot Passowrd')