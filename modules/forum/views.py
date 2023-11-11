from flask import Blueprint, render_template
# print(__name__)
path_forum = Blueprint('forum', __name__, url_prefix='/forum', template_folder='templates', static_folder='static')
# name: views
def index():
    articles = [1, 2, 3]
    return render_template('index.html', posts = articles)
# @path_forum.route('/')
# def hello_world():  # put application's code here
#     return render_template('index.html')
    # return 'Hello World!'


