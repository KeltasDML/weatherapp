from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class loginForm(FlaskForm):
    username = StringField(label='User Name:')
    password = PasswordField(label='Password:')
    login = SubmitField(label='Login')
