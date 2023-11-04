from flask import Blueprint
# print(__name__)
path_forum = Blueprint('forum', __name__, url_prefix='/forum')


@path_forum.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

