from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from ..auth.views.auth import login_request_update
from ..forum.models import Category
from ..forum.models import Article, Classification
from ..auth.models import User
from ..admin.forms import Category_form, Article_form, Classification_form

from Project_public import db

path_admin = Blueprint('admin', __name__, url_prefix='/admin',
                       static_folder='static', template_folder='templates')

@path_admin.route('/')
@login_request_update
def index():
    return render_template('admin/index.html')

@path_admin.route('/category')
@login_request_update
def category_manage_page():
    page = request.args.get('page', 1, type=int)
    # categories = Category.query.order_by(Category.category_id).all()

    pagination = Category.query.order_by(Category.category_id).paginate(page=page, per_page=2, error_out=False)
    categories_show = pagination.items
    return render_template('admin/category.html', categories=categories_show, pagination=pagination)

@path_admin.route('/category/add', methods=['GET','POST'])
@login_request_update
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
@login_request_update
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
@login_request_update
def delete_category(cat_id):
    category_using = Category.query.get(cat_id)
    if category_using:
        db.session.delete(category_using)
        db.session.commit()
        flash(f'Category {category_using.category_name} has been deleted')
        return redirect(url_for('admin.category_manage_page'))

@path_admin.route('/article')
@login_request_update
def article_manage_page():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.article_id).paginate(page=page, per_page=2, error_out=False)
    articles_show = pagination.items
    return render_template('admin/article.html', articles=articles_show, pagination=pagination)

@path_admin.route('/article/add', methods=['GET','POST'])
@login_request_update
def add_new_article():
    form_using = Article_form()
    form_using.category.choices = [(category.category_id, category.category_name) for category in Category.query.all()]
    form_using.classifications.choices = [(cla.cla_id, cla.cla_name) for cla in Classification.query.all()]

    if form_using.validate_on_submit():
        article_creating = Article(
            article_name=form_using.name.data,
            excerpt=form_using.excerpt.data,
            article_status=form_using.status.data,
            category_id=int(form_using.category.data),
            content=form_using.content.data,
            user_id=g.user.user_id


        )
        article_creating.classifications = [Classification.query.get(cla_id) for cla_id in form_using.classifications.data]
        db.session.add(article_creating)
        db.session.commit()
        flash(f'Article {form_using.name.data} has been created')
        return redirect(url_for('admin.article_manage_page'))
    return render_template('admin/add_or_edit_article.html',form= form_using)

@path_admin.route('/article/edit/<int:article_id>', methods=['GET','POST'])
@login_request_update
def edit_article(article_id):
    article_using = Article.query.get(article_id)
    classifications_using = [cla.cla_id for cla in article_using.classifications]
    form_using = Article_form(
        name=article_using.article_name,
        excerpt=article_using.excerpt,
        status=article_using.article_status,
        category=article_using.category.category_id,
        content=article_using.content,
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
        article_using.user_id = g.user.user_id
        article_using.classifications = [Classification.query.get(cla_id) for cla_id in form_using.classifications.data]
        db.session.add(article_using)
        db.session.commit()
        flash(f'Article {form_using.name.data} has been edited')
        return redirect(url_for('admin.article_manage_page'))


    return render_template('admin/add_or_edit_article.html', form=form_using)

@path_admin.route('/article/delete/<int:article_id>', methods=['GET','POST'])
@login_request_update
def delete_article(article_id):
    article_using = Article.query.get(article_id)
    if article_using:
        db.session.delete(article_using)
        db.session.commit()
        flash(f'the article {article_using.article_name} has been deleted')
        return redirect(url_for('admin.article_manage_page'))

@path_admin.route('/class')
@login_request_update
def classification_manage_page():
    page = request.args.get('page', 1, type=int)
    pagination=Classification.query.order_by(Classification.cla_id).paginate(page=page, per_page=20, error_out=False)
    class_showing = pagination.items
    return render_template('admin/cla.html', classifications=class_showing, pagination=pagination)


@path_admin.route('/class/add', methods=['GET','POST'])
@login_request_update
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
@login_request_update
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
@login_request_update
def delete_classification(cla_id):
    classification_using=Classification.query.get(cla_id)
    if classification_using:
        db.session.delete(classification_using)
        db.session.commit()
        flash(f'classification {classification_using.cla_name} has been deleted')
        return redirect(url_for('admin.classification_manage_page'))

@path_admin.route('/user')
@login_request_update
def user_manage_page():
    page=request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.user_id).paginate(page=page, per_page=20, error_out=False)
    users_showing = pagination.items
    return render_template('admin/user.html', users=users_showing, pagination=pagination)






