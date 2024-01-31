from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from werkzeug.security import generate_password_hash
from .models import Article, Category, Classification
from ..auth.models import User
from ..auth.views.auth import login_request_update
from ..forum.forms import Personal_info_edit_form, Change_password_form, Article_form_user
from ..admin.utils import upload_file
from Project_public import db
# print(__name__)
path_forum = Blueprint('forum', __name__, url_prefix='/forum', template_folder='templates', static_folder='static')
# name: views
def index():
    #if you want to have a test, use this: articles_showing = [1, 2, 3]

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.article_id).paginate(page=page, per_page=10, error_out=False)
    articles_showing = pagination.items
    return render_template('index.html', articles = articles_showing, pagination=pagination)
# @path_forum.route('/')
# def hello_world():  # put application's code here
#     return render_template('index.html')
    # return 'Hello World!'

@path_forum.route('/personal')
@login_request_update
def personal_index():
    return render_template('forum/personal_page.html')

@path_forum.route('/personal/edit/info/<int:user_id>', methods=['GET','POST'])
@login_request_update
def personal_info_update(user_id):
    user_using = User.query.get(user_id)
    form_using = Personal_info_edit_form(
        username=user_using.user_name,
        portrait=user_using.head_portrait,
    )
    if form_using.validate_on_submit():
        user_using.user_name = form_using.username.data
        file_update = form_using.portrait.data
        if user_using.head_portrait == file_update:
            user_using.head_portrait = user_using.head_portrait
        else:
            print("pass change")
            portrait_path, portrait_name = upload_file('portrait', file_update)
            file_update.save(portrait_path)
            user_using.head_portrait = f'portrait/{portrait_name}'
        db.session.add(user_using)
        db.session.commit()
        flash(f'basic information of your account {form_using.username.data} has been changed')
        return redirect(url_for('forum.personal_index'))
    return render_template('forum/edit_personal_information.html', form=form_using, user=user_using, key="edit")

@path_forum.route('/personal/password/change', methods=['GET','POST'])
@login_request_update
def personal_change_password():
    user_using = User.query.get(g.user.user_id)
    form_using = Change_password_form()
    if form_using.validate_on_submit():
        if form_using.password.data == form_using.password_confirm.data:
            print('same')
            user_using.password = generate_password_hash(form_using.password.data)
            db.session.add(user_using)
            db.session.commit()
            g.user = user_using
            flash('the password has been changed successfully', 'success')
            return redirect(url_for('forum.personal_change_password'))
        else:
            print('different')
            flash('the two passwords are different', 'fail')
            return redirect(url_for('forum.personal_change_password'))
    return render_template('forum/personal_change_password.html', form=form_using)

@path_forum.route('/personal/articles')
@login_request_update
def personal_article_manage_page():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter_by(user_id=g.user.user_id).order_by(Article.article_id).paginate(page=page, per_page=2, error_out=False)
    articles_show = pagination.items
    return render_template('forum/personal_articles.html', articles=articles_show, pagination=pagination)

@path_forum.route('/personal/article/add', methods=['GET','POST'])
@login_request_update
def personal_add_new_article():
    form_using = Article_form_user()
    form_using.category.choices = [(category.category_id, category.category_name) for category in Category.query.all()]
    form_using.classifications.choices = [(cla.cla_id, cla.cla_name) for cla in Classification.query.all()]


    if form_using.validate_on_submit():
        file = form_using.thumbnail.data
        article_creating = Article(
            article_name=form_using.name.data,
            excerpt=form_using.excerpt.data,
            article_status=form_using.status.data,
            category_id=int(form_using.category.data),
            content=form_using.content.data,
            user_id=g.user.user_id


        )
        if file == None:
            article_creating.thumbnail = None
        else:
            thumbnail_path, thumbnail_name = upload_file('thumbnail', file)
            file.save(thumbnail_path)
            article_creating.thumbnail = f'thumbnail/{thumbnail_name}'
        article_creating.classifications = [Classification.query.get(cla_id) for cla_id in form_using.classifications.data]
        db.session.add(article_creating)
        db.session.commit()
        flash(f'Article {form_using.name.data} has been created')
        return redirect(url_for('forum.personal_article_manage_page'))
    return render_template('forum/personal_add_or_edit_article.html',form= form_using, key="create")

@path_forum.route('/personal/article/edit/<int:article_id>', methods=['GET','POST'])
@login_request_update
def personal_edit_article(article_id):
    article_using = Article.query.get(article_id)
    classifications_using = [cla.cla_id for cla in article_using.classifications]
    form_using = Article_form_user(
        name=article_using.article_name,
        excerpt=article_using.excerpt,
        status=article_using.article_status,
        category=article_using.category.category_id,
        content=article_using.content,
        thumbnail=article_using.thumbnail,
        classifications=classifications_using,
        user_id=g.user.user_id,


    )

    form_using.category.choices = [(category.category_id, category.category_name) for category in Category.query.all()]
    form_using.classifications.choices = [(cla.cla_id, cla.cla_name) for cla in Classification.query.all()]
    if form_using.validate_on_submit():
        article_using.article_name = form_using.name.data
        article_using.excerpt = form_using.excerpt.data
        article_using.article_status = form_using.status.data
        article_using.category_id = int(form_using.category.data)
        article_using.content = form_using.content.data
        file_update = form_using.thumbnail.data
        if article_using.thumbnail == file_update:
            article_using.thumbnail = article_using.thumbnail
        else:
            thumbnail_path, thumbnail_name = upload_file('thumbnail', file_update)
            file_update.save(thumbnail_path)
            article_using.thumbnail = f'thumbnail/{thumbnail_name}'
        article_using.user_id = g.user.user_id
        article_using.classifications = [Classification.query.get(cla_id) for cla_id in form_using.classifications.data]
        db.session.add(article_using)
        db.session.commit()
        flash(f'Article {form_using.name.data} has been edited')
        return redirect(url_for('forum.personal_article_manage_page'))


    return render_template('forum/personal_add_or_edit_article.html', form=form_using, article=article_using, key="edit")

@path_forum.route('/personal/article/delete/<int:article_id>', methods=['GET','POST'])
@login_request_update
def personal_delete_article(article_id):
    article_using = Article.query.get(article_id)
    if article_using:
        db.session.delete(article_using)
        db.session.commit()
        flash(f'the article {article_using.article_name} has been deleted')
        return redirect(url_for('forum.personal_article_manage_page'))


@path_forum.route('/category/<int:cat_id>')
def articles_with_category(cat_id):


    category_using = Category.query.get(cat_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Article.query.filter(Article.category_id == cat_id).paginate(page=page, per_page=2, error_out=False)
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

@path_forum.route('/search')
def search():
    words = request.args.get('words')
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter(Article.article_name.like("%"+words+"%")).paginate(page=page, per_page=2, error_out=False)
    articles_using = pagination.items
    return render_template('forum/index_with_search.html', words=words, articles=articles_using, pagination=pagination)































