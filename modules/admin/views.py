from flask import Blueprint, render_template, request
from ..auth.views.auth import login_request_update
from ..forum.models import Category

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

    categories = Category.query.order_by(Category.category_id).paginate(page=page, per_page=50, error_out=False)
    print(categories)
    return render_template('admin/category.html')
