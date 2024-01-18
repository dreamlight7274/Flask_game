from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, Length
# from .models import Article
from ..forum.models import ArticleStatus
class Category_form(FlaskForm):
    name = StringField('Category_name', validators=[
        DataRequired(message="please input the name of the category"),
        Length(max=100, message="the length of the name of category should be less than 100 words")
    ])
    slug = StringField('Category_slug', validators=[
        DataRequired(message="please input the slug of the category"),
        Length(max=100, message="the length of the slug of category should be less than 100 words")
    ])

class Article_form(FlaskForm):
    name = StringField('name', validators=[
        DataRequired(message="please input the title"),
        Length(max=30, message="the length of the name of article should less than 30 words")
    ])
    excerpt = StringField('excerpt', validators=[
        DataRequired(message="please input the excerpt of the article"),
        Length(max=100, message="The length of the excerpt of article should less than 100 words")
    ])
    status = RadioField('status',
                        choices=(ArticleStatus.draft.name, ArticleStatus.online.name),
                        default=ArticleStatus.online.name)
    category = SelectField('category', choices=None, coerce=int, validators=[
        DataRequired(message="please input the category"),
    ])
    content = TextAreaField('content', validators=[
        DataRequired(message="Please input the content of article")
    ])
    classifications = SelectMultipleField('classifications', choices=None, coerce=int)

class Classification_form(FlaskForm):
    name = StringField('name', validators=[
        DataRequired(message="please input the name of classification"),
        Length(max=50, message="The length of the name should be less than 50 words")
    ])