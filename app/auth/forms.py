from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('e-mail', validators=[DataRequired(), Length(1, 100), Email()])
    
    # TODO: add REGEX to username
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