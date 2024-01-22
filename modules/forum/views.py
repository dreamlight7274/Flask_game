from flask import Blueprint, render_template, request
from .models import Article, Category
from ..auth.models import User

# print(__name__)
path_forum = Blueprint('forum', __name__, url_prefix='/forum', template_folder='templates', static_folder='static')
# name: views
def index():
    #if you want to have a test, use this: articles_showing = [1, 2, 3]

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.article_id).paginate(page=page, per_page=1, error_out=False)
    articles_showing = pagination.items
    return render_template('index.html', articles = articles_showing, pagination=pagination)
# @path_forum.route('/')
# def hello_world():  # put application's code here
#     return render_template('index.html')
    # return 'Hello World!'

@path_forum.route('/category/<int:cat_id>')
def articles_with_category(cat_id):


    category_using = Category.query.get(cat_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Article.query.filter(Article.category_id == cat_id).paginate(page=page, per_page=5, error_out=False)
    articles_showing = pagination.items
    return render_template('forum/articles_with_cat.html', articles=articles_showing, category=category_using, pagination=pagination)

@path_forum.route('/article/<int:cat_id>/<int:article_id>')
def article_detail(cat_id, article_id):
    article_using = Article.query.get(article_id)
    category_using = Category.query.get(cat_id)
    user_using = User.query.get(article_using.user_id)
    previous_one = Article.query.filter(Article.article_id < article_id).order_by(-Article.article_id).first()
    next_one = Article.query.filter(Article.article_id > article_id).order_by(Article.article_id).first()
    return render_template('forum/article_detail.html', category=category_using, article=article_using, user=user_using,
                           previous_one=previous_one, next_one=next_one)



