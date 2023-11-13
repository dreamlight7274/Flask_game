from flask import Blueprint, render_template, request

path_auth = Blueprint('auth', __name__, url_prefix='/auth',
                      static_folder='../static', template_folder='../templates')
@path_auth.route('/login', methods=['GET', 'POST']) # method support
def login():
    if request.method == 'POST':
            print(request.form.get('username'))
    return render_template('login.html')

@path_auth.route('/register', methods=['GET', 'POST']) # method support
def register():
    return render_template('register.html')