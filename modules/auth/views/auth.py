from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g, abort
from ..models import User
from werkzeug.security import check_password_hash, generate_password_hash
from Project_public import db
from ..forms import LoginForm, RegisterForm
import functools


path_auth = Blueprint('auth', __name__, url_prefix='/auth',
                      static_folder='../static', template_folder='../templates')
# before the request of url
@path_auth.before_app_request
def user_log_in_status():

    user_id = session.get('user_id')

    # urls_admin = ['/admin/']
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(int(user_id))
# g, a global object, it can be used everywhere
        if g.user.is_admin:
            g.user.perm = 2
        elif not g.user.is_admin:
            g.user.perm = 1

def login_required(view):
    @functools.wraps(view)
    def warpped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return warpped_view
# OK, if you want to have a check whether the user has log in, user this decorate

def login_request_update(view):
    @functools.wraps(view)
    def warpped_view(**kwargs):
        if g.user is None:
            redirect_direction = f"{url_for('auth.login')}?redirect_direction={request.path}"
            return redirect(redirect_direction)

        return view(**kwargs)
    return warpped_view
# if you are not login, go to login page, and if you follow the login in path, it will lead you to the page you want to
# go to

def admin_request(view):
    @functools.wraps(view)
    def warpped_view(**kwargs):
        if g.user is None:
            redirect_direction = f"{url_for('auth.login')}?redirect_direction={request.path}"
            return redirect(redirect_direction)
        if g.user.perm != 2:
            abort(403, "You don't have privileges to access this page")

        return view(**kwargs)

    return warpped_view

def owner_request(view):
    @functools.wraps(view)
    def warpped_view(**kwargs):
        if g.user is None:
            redirect_direction = f"{url_for('auth.login')}?redirect_direction={request.path}"
            return redirect(redirect_direction)
        if g.user.user_id != request.args.get('user_id'):
            abort(403, "You don't have privileges to access this page")

        return view(**kwargs)

    return warpped_view
@path_auth.route('/login', methods=['GET', 'POST']) # method support
def login():
    # if request.method == 'POST':
    #     print(request.form.get('username'))
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     error = None
    #
    #     user_exist = User.query.filter_by(user_name=username).first()
    #     if user_exist is None:
    #         error = 'The user is not exist'
    #         flash('The user is not exist')
    #     elif not check_password_hash(user_exist.password, password):
    #         error = 'Password is not correct'
    #         flash('The password is not correct')
    #
    #     if error is None:
    #         session.clear()
    #         session['user_id'] = user_exist.user_id
    #         return redirect('/')
    # the approach without form
    redirect_direction = request.args.get('redirect_direction')

    form_login = LoginForm()
    if form_login.validate_on_submit():
        user = User.query.filter_by(user_name=form_login.username.data).first()
        session.clear()
        session['user_id'] = user.user_id
        if redirect_direction is not None:
            return redirect(redirect_direction)
        # if there is such a parameter redirect_Direction, get the path and go to that page
        return redirect('/')




    return render_template('login.html', form= form_login)

@path_auth.route('/register', methods=['GET', 'POST']) # method support
def register():

    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     password_confirm = request.form.get('password_confirm')
    #     exit_user = User.query.filter_by(user_name=username).first()
    #
    #     if password != password_confirm:
    #         flash('the two passwords are different')
    #         return redirect(url_for('auth.register'))
    #
    #
    #     if exit_user:
    #         flash('The username have been used')
    #         return redirect(url_for('auth.register'))
    #     else:
    #         user_insert = User(user_name= username, password=generate_password_hash(password))
    #         db.session.add(user_insert)
    #         db.session.commit()
    #         session.clear()
    #         session['user_id'] = user_insert.user_id
    #     return redirect('/')
    # approach without form
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        user_insert = User(user_name=form_register.username.data, password=generate_password_hash(form_register.password.data))
        db.session.add(user_insert)
        db.session.commit()
        session.clear()
        session['user_id'] = user_insert.user_id
        return redirect('/')

    return render_template('register.html', form= form_register)
@path_auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')