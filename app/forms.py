from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError
from wtforms_components import TimeField

class BusForm(FlaskForm):
    bus = StringField('Bus number', validators=[DataRequired()])
    timing = TimeField('What is the required timing', validators=[DataRequired()])
    weekday = RadioField(choices=[("wd","Weekday"),("we","Weekend")])
    submit = SubmitField('Submit')

    def validate_bus(self,bus):
        if bus.data not in ['10','158','12']:# dummy bus numbers
            raise ValidationError("That is not a valid bus number")

            
