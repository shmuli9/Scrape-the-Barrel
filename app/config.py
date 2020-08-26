import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "86b64bc9a1dff9f00c7b229c3515bc009e0cf3319f07864e"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MIGRATIONS_DIR = "migrations"

    USER_APP_NAME = "Scraping the Barrel"

    MASTER_URL_PREFIX = "/"
