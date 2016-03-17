from flask.ext.wtf import Form
from flask.ext.wtf.html5 import URLField
from wtforms import TextField, StringField, BooleanField, validators
from wtforms.validators import DataRequired, url

class get_swtIDForm(Form):
   usr_name = StringField('usr_name', validators=[DataRequired()])
   remember_me = BooleanField('remember_me', default=False)

class MyForm(Form):
   usr_name = StringField('usr_name', validators=[DataRequired()])

class LoginForm(Form):
   usr_name = StringField('usr_name', validators=[DataRequired()])
   remember_me = BooleanField('remember_me', default=False)

class InputURLform(Form):
   url = URLField('URL of source page to be changed', 
   	validators=[url()])
