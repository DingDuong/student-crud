from flask_wtf import FlaskForm
from wtforms import StringField, validators

class StudentForm(FlaskForm):
  first_name = StringField('First Name', [validators.DataRequired()])
  last_name = StringField('Last Name', [validators.DataRequired()])
