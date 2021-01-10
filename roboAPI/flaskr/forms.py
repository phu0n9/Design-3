from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField,
                     IntegerField,
                     DateTimeField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from wtforms import StringField, TextField, SubmitField
from wtforms.fields.html5 import DateField
from datetime import *
from wtforms.widgets.html5 import DateTimeLocalInput


class userSearch(FlaskForm):   
    
    name = StringField('Name')
    submit = SubmitField('Search')
 
 
    
class carSearch(FlaskForm):
    """Car search form. for users"""
    make = StringField('Make')
    body = StringField('Body Type')
    colour = SelectField('Colour', 
                        choices=[('', 'Any'),
                        	  ('red', 'Red'),
                                 ('green', 'Green'),
                                 ('blue', 'Blue'),
                                 ('black', 'Black'),
                                 ('white', 'White'),
                                 ('silver', 'Silver'),
                                 ('other', 'Other')])
    seats = SelectField('Seats',
                        choices=[('', 'Any'),
                        	  ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = StringField('Cost')
    start = StringField('Start', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    end = StringField('End', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    page = StringField('page')
    submit = SubmitField('Search')
