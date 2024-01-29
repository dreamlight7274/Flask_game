from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, SelectMultipleField, PasswordField, BooleanField
from flask_wtf.file import FileField, file_size, file_allowed
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
    thumbnail = FileField("thumbnail", validators=[
        file_allowed(['jpg','jpeg','png'], message="only jpg/jpeg/png file are available"),
        file_size(max_size=10240000, message="The size of the thumbnail should be less than 10 MB")
    ], description="the size of the thumbnail should be less than 10 MB, and jpg/jpeg/png files are accessible ")
    classifications = SelectMultipleField('classifications', choices=None, coerce=int)

class Classification_form(FlaskForm):
    name = StringField('name', validators=[
        DataRequired(message="please input the name of classification"),
        Length(max=50, message="The length of the name should be less than 50 words")
    ])


class User_form(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message="Please input the username"),
        Length(max=20, message="the length of the username should be less than 20 words")
    ])
    password = PasswordField('password', validators=[
        Length(min=10, max=30, message="password should be less than 30 words and more than 10 words")

    ], description="It's the password")

    portrait = FileField("portrait", validators=[
        file_allowed(['jpg','jpeg','png'], message="only jpg/jpeg/png file are available"),
        file_size(max_size=10240000, message="The size of the portrait should be less than 10 MB")


    ], description="the size of the portrait should be less than 10 MB, and jpg/jpeg/png files are accessible ")
    is_VIP = BooleanField("is_VIP", default=False)
    is_admin = BooleanField("is_admin", default=False)

class User_edit_form(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message="Please input the username"),
        Length(max=20, message="the length of the username should be less than 20 words")
    ])
    password = PasswordField('password', validators=[
        Length(max=30, message="password should be less than 30 words and more than 10 words")

    ], description="It's the password, if it's empty, the password won't be changed")

    portrait = FileField("portrait", validators=[
        file_allowed(['jpg','jpeg','png'], message="only jpg/jpeg/png file are available"),
        file_size(max_size=10240000, message="The size of the portrait should be less than 10 MB")
    ], description="the size of the portrait should be less than 10 MB, and jpg/jpeg/png files are accessible ")

    is_VIP = BooleanField("is_VIP", default=False)
    is_admin = BooleanField("is_admin", default=False)