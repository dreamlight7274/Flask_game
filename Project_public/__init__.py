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
    from modules.forum import models

    app.register_blueprint(path_forum)


    return app

    # app = Flask(__name__)
    # @app.route('/')
    # def hello_world():  # put application's code here
    #     return 'Hello World!'

