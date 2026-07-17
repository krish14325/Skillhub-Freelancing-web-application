from wtforms import( 
    StringField,
    TextAreaField,
    IntegerField,
    SubmitField,
    EmailField,
    PasswordField
)

from flask_wtf import FlaskForm

from wtforms.validators import(
    DataRequired
)

class ProfileForm(FlaskForm):
    company_name = StringField("Company Name" , validators=[DataRequired()])
    company_logo = StringField("Company logo" , validators=[DataRequired()])
    website = StringField("Website" , validators=[DataRequired()])
    description = StringField("Description" , validators=[DataRequired()])
    submit = SubmitField("Create Profile")