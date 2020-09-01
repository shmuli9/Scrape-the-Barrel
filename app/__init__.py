import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.commands import db_cli
from app.config import Config

migrate = Migrate()
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, config_class.MIGRATIONS_DIR)
    app.cli.add_command(db_cli)

    from app.routes import app as bp
    app.register_blueprint(bp, url_prefix=app.config["MASTER_URL_PREFIX"] + bp.url_prefix)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(f'logs/{app.config["USER_APP_NAME"]}.log', maxBytes=2048, backupCount=30)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info(f'{app.config["USER_APP_NAME"]} Startup')

    return app
