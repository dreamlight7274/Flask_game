from flask import Blueprint, render_template
from ..auth.views.auth import login_request_update


path_admin = Blueprint('admin', __name__, url_prefix='/admin',
                       static_folder='static', template_folder='templates')

@path_admin.route('/')
@login_request_update
def index():
    return render_template('admin/index.html')
