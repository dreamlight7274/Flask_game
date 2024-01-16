from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..auth.views.auth import login_request_update
from ..forum.models import Category
from ..admin.forms import Category_form
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


