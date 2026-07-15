from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SubmitField,
    TextAreaField , 
    IntegerField
)
from wtforms.validators import DataRequired

class ProfileForm(FlaskForm):
    full_name = StringField("Full Name" , validators=[DataRequired()])
    Bio = TextAreaField("Bio" , validators=[DataRequired()])
    skills = TextAreaField("Skills" , validators=[DataRequired()])
    experience = StringField("Experience" , validators=[DataRequired()])
    education = StringField("Education" , validators=[DataRequired()])
    hourly_rate = IntegerField("Hourly Rate" , validators=[DataRequired()])
    country = StringField("Country" , validators=[DataRequired()])
    city = StringField("City" , validators=[DataRequired()])
    linkedin = StringField("Linkedin" , validators=[DataRequired()])
    github = StringField("GitHub" , validators=[DataRequired()])
    portfolio = StringField("Portfolio" , validators=[DataRequired()])
    submit = SubmitField("Submit")

