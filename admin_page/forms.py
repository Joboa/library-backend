from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  email = EmailField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')
  