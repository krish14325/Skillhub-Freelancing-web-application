from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)

class RegisterationForm(FlaskForm):
    username = StringField("Username", validators=[ DataRequired() , Length(min=3 , max=100)])
    email = EmailField("Email", validators=[ DataRequired() , Email()])
    password = PasswordField("Password", validators=[ DataRequired() , Length(min=6)])
    confirm_password = PasswordField("Confirm_Password", validators=[ DataRequired() , EqualTo("password" , message="Password Must Match.")])
    role = SelectField("Role", choices=[("client" , "Client"),("freelancer" , "Freelancer")] , validators=[DataRequired()])
    submit = SubmitField("Register")
