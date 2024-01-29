from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, SelectMultipleField, PasswordField, BooleanField
from flask_wtf.file import FileField, file_size, file_allowed
from wtforms.validators import DataRequired, Length

class Personal_info_edit_form(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message="Please input the username"),
        Length(max=20, message="the length of the username should be less than 20 words")
    ])
    portrait = FileField("portrait", validators=[
        file_allowed(['jpg','jpeg','png'], message="only jpg/jpeg/png file are available"),
        file_size(max_size=10240000, message="The size of the portrait should be less than 10 MB")
    ], description="the size of the portrait should be less than 10 MB, and jpg/jpeg/png files are accessible ")