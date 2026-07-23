from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SubmitField,
    TextAreaField , 
    SelectField,
    IntegerField,
    FileField
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
    
class ServiceForm(FlaskForm):
    title = StringField("Service Title" , validators=[DataRequired()])
    description = StringField("Description" , validators=[DataRequired()])
    price = IntegerField("Price" , validators=[DataRequired()])
    delivery_time = StringField("Delivery Time" , validators=[DataRequired()])
    category = StringField("Category" , validators=[DataRequired()])
    service_image = StringField("Service Image" , validators=[DataRequired()])
    submit = SubmitField("Add Service" , validators=[DataRequired()])

class UploadForm(FlaskForm):
    project_file = FileField("Upload File" , validators=[DataRequired()])
    submit = SubmitField("Submit" , validators=[DataRequired()])
    