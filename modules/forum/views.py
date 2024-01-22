from flask import Blueprint, render_template, request

# print(__name__)
path_forum = Blueprint('forum', __name__, url_prefix='/forum', template_folder='templates', static_folder='static')
# name: views
def index():
    #if you want to have a test, use this: articles_showing = [1, 2, 3]
    from modules.forum.models import Article
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.article_id).paginate(page=page, per_page=10, error_out=False)
    articles_showing = pagination.items
    return render_template('index.html', articles = articles_showing, pagination=pagination)
# @path_forum.route('/')
# def hello_world():  # put application's code here
#     return render_template('index.html')
    # return 'Hello World!'


