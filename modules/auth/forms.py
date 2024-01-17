# import flask_wtf to verify the data the user import
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from werkzeug.security import check_password_hash
from .models import User


class LoginForm(FlaskForm):
    def username_log(username):
        user_input = f'the user log in is  {username}'
        print(user_input)
        return username
    # we use filter to make a pre-action on the data we input
    username = StringField('username', validators=[
        DataRequired(message="please input the username"),
        # Length(max=30, message='the username should be less than 30 words')
        ], filters=(username_log,))
    # "," is important

    password = PasswordField('password', validators=[
        DataRequired(message="please input the password"),
        # Length(min=2, max=30, message="The password should be more than 10 words and less than 30 words")
        ])
    def validate_username(form, field):
        user = User.query.filter_by(user_name=field.data).first()
        if user is None:
            error = 'the user is not exist, please check the username.'
            raise ValidationError(error)
        elif not check_password_hash(user.password, form.password.data):
            error = 'there is somthing wrong with your username or the password'
            raise ValidationError(error)

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message="please input the username"),
        Length(max=20, message="the username should be less than 30 words")
        ])
    password = PasswordField('password', validators=[
        DataRequired(message="please input the password"),
        Length(min=10, max=30, message="the password should be more than 10 words and less than 30 words"),
        EqualTo('password_confirm', message="The two passwords are inconsistent")
        ])
    password_confirm = PasswordField('password_confirm')

    def validate_username(form, field):
        user = User.query.filter_by(user_name=field.data).first()
        if user is not None:
            error = 'the user is exist.'
            raise  ValidationError(error)




