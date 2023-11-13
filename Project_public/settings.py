from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve()
PROJECT_PATH = Path(__file__).resolve().parent.parent
# we should get the path of our file: settings, absolute path, so, use resolve,


# print(DEFAULT_PATH)

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/forum'
SECRET_KEY = 'BANGZHAOTEST%'
# for session

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
# update automatically
