from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError, Optional
from wtforms_components import TimeField
import datetime
from app.bus import bus_available

class BusForm(FlaskForm):
    bus = StringField('Bus number', validators=[DataRequired()])
    timing = TimeField('What is the required timing', validators=[Optional()],
        default = datetime.datetime.now().time())
    weekday = RadioField(choices=[("weekday","Weekday"),("weekend","Weekend")],
        validators=[DataRequired()])
    from_busstop = StringField("Which busstop are you at")
    to_busstop = StringField("Which busstop are you going towards")
    submit = SubmitField('Submit')

    def validate_bus(self,bus):
        if not bus_available(bus.data):
            raise ValidationError("That is not a valid bus number")