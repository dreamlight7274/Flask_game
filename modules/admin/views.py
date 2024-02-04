from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import upload_file
from ..auth.views.auth import admin_request
from ..forum.models import Category
from ..forum.models import Article, Classification, Comment
from ..auth.models import User
from ..admin.forms import Category_form, Article_form, Classification_form, User_form, User_edit_form

from Project_public import db

path_admin = Blueprint('admin', __name__, url_prefix='/admin',
                       static_folder='static', template_folder='templates')

@path_admin.route('/')
@admin_request
def index():
    return render_template('admin/index.html')

@path_admin.route('/category')
@admin_request
def category_manage_page():
    page = request.args.get('page', 1, type=int)
    # categories = Category.query.order_by(Category.category_id).all()

    pagination = Category.query.order_by(Category.category_id).paginate(page=page, per_page=2, error_out=False)
    categories_show = pagination.items
    return render_template('admin/category.html', categories=categories_show, pagination=pagination)

@path_admin.route('/category/add', methods=['GET','POST'])
@admin_request
def add_new_category():
    form_using = Category_form()
    if form_using.validate_on_submit():
        new_category = Category(category_name=form_using.name.data, category_slug=form_using.slug.data)
        db.session.add(new_category)
        db.session.commit()
        flash(f'{form_using.name.data} has been added to the database')
        return redirect(url_for('admin.category_manage_page'))
    return render_template('admin/add_or_edit_category.html', form=form_using)

@path_admin.route('/category/edit/<int:cat_id>', methods=['GET','POST'])
@admin_request
def edit_category(cat_id):
    category_using = Category.query.get(cat_id)
    form_using = Category_form(name=category_using.category_name, slug=category_using.category_slug)
    if form_using.validate_on_submit():
        category_using.category_name = form_using.name.data
        category_using.category_slug = form_using.slug.data
        db.session.add(category_using)
        db.session.commit()
        flash(f'Category {form_using.name.data} has been changed')
        return redirect(url_for('admin.category_manage_page'))
    return render_template('admin/add_or_edit_category.html', form=form_using)

@path_admin.route('/category/delete/<int:cat_id>', methods=['GET','POST'])
@admin_request
def delete_category(cat_id):
    category_using = Category.query.get(cat_id)
    if category_using:
        db.session.delete(category_using)
        db.session.commit()
        flash(f'Category {category_using.category_name} has been deleted')
        return redirect(url_for('admin.category_manage_page'))

@path_admin.route('/article')
@admin_request
def article_manage_page():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.article_id).paginate(page=page, per_page=2, error_out=False)
    articles_show = pagination.items
    return render_template('admin/article.html', articles=articles_show, pagination=pagination)

@path_admin.route('article/date/<string:date>')
@admin_request
def article_with_date_manage_page(date):
    import re
#     use to devide the string
    date_rule = re.compile(r'\d{4}|\d{2}')
    # 2-digit number and 4-digit number
    dates = date_rule.findall(date)
    print(dates)
    from sqlalchemy import extract, and_
    page=request.args.get('page', 1, type=int)
    articles_using = Article.query.filter(
        and_(
            extract('year', Article.public_date) == int(dates[1]),
            extract('month', Article.public_date) == int(dates[0])
        )
    )
    pagination = articles_using.paginate(page=page, per_page=2, error_out=False)
    return render_template('/admin/article_with_date.html', articles=pagination.items, pagination=pagination, date=date)








@path_admin.route('/article/add', methods=['GET','POST'])
@admin_request
def add_new_article():
    form_using = Article_form()
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
        return redirect(url_for('admin.article_manage_page'))
    return render_template('admin/add_or_edit_article.html',form= form_using, key="create")

@path_admin.route('/article/edit/<int:article_id>', methods=['GET','POST'])
@admin_request
def edit_article(article_id):
    article_using = Article.query.get(article_id)
    classifications_using = [cla.cla_id for cla in article_using.classifications]
    form_using = Article_form(
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
        return redirect(url_for('admin.article_manage_page'))


    return render_template('admin/add_or_edit_article.html', form=form_using, article=article_using, key="edit")

@path_admin.route('/article/delete/<int:article_id>', methods=['GET','POST'])
@admin_request
def delete_article(article_id):
    article_using = Article.query.get(article_id)
    if article_using:
        db.session.delete(article_using)
        db.session.commit()
        flash(f'the article {article_using.article_name} has been deleted')
        return redirect(url_for('admin.article_manage_page'))

@path_admin.route('/class')
@admin_request
def classification_manage_page():
    page = request.args.get('page', 1, type=int)
    pagination=Classification.query.order_by(Classification.cla_id).paginate(page=page, per_page=20, error_out=False)
    class_showing = pagination.items
    return render_template('admin/cla.html', classifications=class_showing, pagination=pagination)


@path_admin.route('/class/add', methods=['GET','POST'])
@admin_request
def add_new_classification():
    form_using = Classification_form()
    if form_using.validate_on_submit():
        classification_creating = Classification(cla_name=form_using.name.data)
        db.session.add(classification_creating)
        db.session.commit()
        flash(f'classification {form_using.name.data} has been added')
        return redirect(url_for('admin.classification_manage_page'))
    return render_template('admin/add_or_edit_cla.html', form=form_using)

@path_admin.route('class/edit/<int:cla_id>', methods=['GET','POST'])
@admin_request
def edit_classification(cla_id):
    classification_using = Classification.query.get(cla_id)
    form_using = Classification_form(name=classification_using.cla_name)
    if form_using.validate_on_submit():
        classification_using.cla_name = form_using.name.data
        db.session.add(classification_using)
        db.session.commit()
        flash(f'classification {form_using.name.data} has been edited')
        return redirect(url_for('admin.classification_manage_page'))
    return render_template('admin/add_or_edit_cla.html', form=form_using)

@path_admin.route('class/delete/<int:cla_id>', methods=['GET','POST'])
@admin_request
def delete_classification(cla_id):
    classification_using=Classification.query.get(cla_id)
    if classification_using:
        db.session.delete(classification_using)
        db.session.commit()
        flash(f'classification {classification_using.cla_name} has been deleted')
        return redirect(url_for('admin.classification_manage_page'))

@path_admin.route('/user')
@admin_request
def user_manage_page():
    page=request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.user_id).paginate(page=page, per_page=20, error_out=False)
    users_showing = pagination.items
    return render_template('admin/user.html', users=users_showing, pagination=pagination)

@path_admin.route('/user/add', methods=['GET','POST'])
@admin_request
def add_new_user():
    form_using = User_form()

    if form_using.validate_on_submit():
        file = form_using.portrait.data
        user_creating = User(
            user_name=form_using.username.data,
            password=generate_password_hash(form_using.password.data),
            is_VIP=form_using.is_VIP.data,
            is_admin=form_using.is_admin.data
        )
        if file is not None:
            portrait_path, portrait_name = upload_file('portrait', file)
            file.save(portrait_path)
            user_creating.head_portrait=f'portrait/{portrait_name}'
        db.session.add(user_creating)
        db.session.commit()
        flash(f'User {form_using.username.data} has been created')
        return redirect(url_for('admin.user_manage_page'))

    return render_template('admin/add_or_edit_user.html', form=form_using, key="create")

@path_admin.route('/user/edit/<int:user_id>', methods=['GET','POST'])
@admin_request
def edit_user(user_id):
    user_using = User.query.get(user_id)
    print("h1")
    form_using = User_edit_form(
        username=user_using.user_name,
        password=user_using.password,
        portrait=user_using.head_portrait,
        is_VIP=user_using.is_VIP,
        is_admin=user_using.is_admin
    )
    print("h1")
    print(form_using.portrait.data)
    if form_using.validate_on_submit():
        print("h1")
        user_using.user_name = form_using.username.data
        if not form_using.password.data:
            print("here pass not")
            user_using.password = user_using.password
        else:
            print("pass have")
            user_using.password = generate_password_hash(form_using.password.data)

        file_update = form_using.portrait.data
        if user_using.head_portrait == file_update:
            print("por no change")
            user_using.head_portrait = user_using.head_portrait
        else:
            print("pass change")
            portrait_path, portrait_name = upload_file('portrait', file_update)
            file_update.save(portrait_path)
            user_using.head_portrait = f'portrait/{portrait_name}'
        user_using.is_VIP = form_using.is_VIP.data
        user_using.is_admin = form_using.is_admin.data
        db.session.add(user_using)
        db.session.commit()
        flash(f'The data of User{form_using.username.data} has been changed')
        return redirect(url_for('admin.user_manage_page'))

    return render_template('admin/add_or_edit_user.html', form=form_using, user=user_using, key="edit")

@path_admin.route('/user/delete/<int:user_id>', methods=['GET','POST'])
@admin_request
def delete_user(user_id):
    user_using = User.query.get(user_id)
    if user_using:
        db.session.delete(user_using)
        db.session.commit()
        flash(f'User {user_using.user_name} has been deleted')
        return redirect(url_for('admin.user_manage_page'))

@path_admin.route('/comment')
@admin_request
def comment_manage_page():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.comment_id).paginate(page=page, per_page=3, error_out=False)
    comments_showing = pagination.items
    return render_template('admin/comment.html', comments=comments_showing, pagination=pagination)
@path_admin.route('/comment/delete/<int:comment_id>', methods=['GET','POST'])
@admin_request
def delete_comment(comment_id):
    comment_using = Comment.query.get(comment_id)
    if comment_using:
        db.session.delete(comment_using)
        db.session.commit()
        flash(f'Comment has been deleted')
        return redirect(url_for('admin.comment_manage_page'))

@path_admin.context_processor
def dates_classification():
    articles_using = Article.query.order_by(Article.public_date)
    dates = set([article.public_date.strftime("%m_%Y") for article in articles_using])

    return dict(dates=dates)


