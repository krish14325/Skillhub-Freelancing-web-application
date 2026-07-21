from wtforms import( 
    StringField,
    TextAreaField,
    IntegerField,
    SubmitField,
    EmailField,
    SelectField,
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
    
class ReviewForm(FlaskForm):
    rating= SelectField(
        "Rating" , choices=[
            ("1" , "⭐"),
            ("2" , "⭐⭐"),
            ("3" , "⭐⭐⭐"),
            ("4" , "⭐⭐⭐⭐"),
            ("5" , "⭐⭐⭐⭐⭐")
        ] , 
        validators=[DataRequired()]
    )
    comment = TextAreaField("Comment" , validators=[DataRequired()])
    submit = SubmitField("Sumit Review")