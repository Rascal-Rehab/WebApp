from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = StringField('Organization', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Continue')