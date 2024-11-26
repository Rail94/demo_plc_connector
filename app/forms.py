from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')

class CreateProjectForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    piva = StringField('Company PIVA', validators=[DataRequired()])
    address = StringField('Company Address', validators=[DataRequired()])
    description = TextAreaField('Project Description', validators=[DataRequired()])
    accepted = BooleanField('Project Accepted')
    submit = SubmitField('Create')
    
class EditProjectForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    piva = StringField('Company PIVA', validators=[DataRequired()])
    address = StringField('Company Address', validators=[DataRequired()])
    description = TextAreaField('Project Description', validators=[DataRequired()])
    accepted = BooleanField('Project Accepted')
    submit = SubmitField('Save')