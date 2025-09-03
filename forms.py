from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

# create Registration Form for Users
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=25)])
    submit = SubmitField('Register')

# create Login Form for Users
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=25)])
    submit = SubmitField('Login')
