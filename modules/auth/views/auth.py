from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g
from ..models import User
from werkzeug.security import check_password_hash, generate_password_hash
from Project_public import db


path_auth = Blueprint('auth', __name__, url_prefix='/auth',
                      static_folder='../static', template_folder='../templates')
# before the request of url
@path_auth.before_app_request
def user_log_in_status():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(int(user_id))
# g, a global object, it can be used everywhere

@path_auth.route('/login', methods=['GET', 'POST']) # method support
def login():
    if request.method == 'POST':
        print(request.form.get('username'))
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        user_exist = User.query.filter_by(user_name=username).first()
        if user_exist is None:
            error = 'The user is not exist'
            flash('The user is not exist')
        elif not check_password_hash(user_exist.password, password):
            error = 'Password is not correct'
            flash('The password is not correct')

        if error is None:
            session.clear()
            session['user_id'] = user_exist.user_id
            return redirect('/')




    return render_template('login.html')

@path_auth.route('/register', methods=['GET', 'POST']) # method support
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        exit_user = User.query.filter_by(user_name=username).first()

        if password != password_confirm:
            flash('the two passwords are different')
            return redirect(url_for('auth.register'))


        if exit_user:
            flash('The username have been used')
            return redirect(url_for('auth.register'))
        else:
            user_insert = User(user_name= username, password=generate_password_hash(password))
            db.session.add(user_insert)
            db.session.commit()
            session.clear()
            session['user_id'] = user_insert.user_id
        return redirect('/')

    return render_template('register.html')
@path_auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')