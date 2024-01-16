from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
class Category_form(FlaskForm):
    name = StringField('Category_name', validators=[
        DataRequired(message="please input the name of the category"),
        Length(max=100, message="the length of the name of category should be less than 100 words")
    ])
    slug = StringField('Category_slug', validators=[
        DataRequired(message="please input the slug of the category"),
        Length(max=100, message="the length of the slug of category should be less than 100 words")
    ])
