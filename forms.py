from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField, ValidationError
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class PetForm(FlaskForm):

    name = StringField("Pet Name", validators=[InputRequired()])

    species = SelectField("Species", 
                          choices=[('Cat','Cat'),('Dog','Dog'),('Porcupine','Porcupine')], 
                          validators=[InputRequired()])

    photo_url = StringField("Pet Photo", validators=[Optional(), URL()])

    age = IntegerField("Pet Age", validators=[Optional(), NumberRange(min=0, max=30)])

    notes = StringField("Notes", validators=[Optional()])

    available = BooleanField("Availability", default=True)