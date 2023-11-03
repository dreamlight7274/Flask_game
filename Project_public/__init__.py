from flask import Flask
import os



def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
# first, we should tell something to the system, hi, I want to design the configuration by myself.
# update the configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # sometimes, we need some test config, so we should give him or her a space
    if test_config is None:
        # If there is no settings, use setting.py, if there is no setting.py, don't give error message.
        app.config.from_pyfile('settings.py', silent=True)
    else:
        # if there is no setting.py, use test_config
        app.config.from_mapping(test_config)


    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
# make direcotry, or if it is existing, skip it, I don't know if it will help me. make be it will be useful
# in the future

    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'
    return app

    # app = Flask(__name__)
    # @app.route('/')
    # def hello_world():  # put application's code here
    #     return 'Hello World!'

