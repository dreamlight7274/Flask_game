from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Project_public import settings
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
# first, we should tell something to the system, hi, I want to design the configuration by myself.
# update the configuration



    # sometimes, we need some test config, so we should give him or her a space
    if test_config is None:
        CONFIG_PATH = settings.DEFAULT_PATH
        # If there is no test settings, use setting.py, if there is no setting.py, don't give error message.
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # if there is no setting.py, use test_config
        app.config.from_mapping(test_config)
    db.init_app(app)
    migrate.init_app(app, db)

    # flask db init
    # flask db migrate
    # flask db upgrade

    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
# make direcotry, or if it is existing, skip it, I don't know if it will help me. make be it will be useful
# in the future
    from modules.forum.views import path_forum
    from modules.auth import views as auth_views
    from modules.forum.views import index
    from modules.admin import views as admin_views

    from modules.forum import models
    from modules.auth import models




    app.register_blueprint(path_forum)
    app.register_blueprint(auth_views.path_auth)
    app.register_blueprint(admin_views.path_admin)
    # add another rule for index, the path is not so good with forum here
    app.add_url_rule('/', endpoint='index', view_func=index) # don't add "()"
    app.context_processor(inject_categories)


    return app
    # app = Flask(__name__)
    # @app.route('/')
    # def hello_world():  # put application's code here
    #     return 'Hello World!'

def inject_categories():
    from modules.forum.models import Category
    categories = Category.query.all()
    return dict(categories=categories)
# always we need categories, so we return it to all the templates




