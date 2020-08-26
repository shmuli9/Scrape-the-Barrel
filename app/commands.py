import os
import shutil

import click
import flask_migrate
from flask.cli import AppGroup

from app.config import Config

db_cli = AppGroup('local', help="Commands to help with local dev config")

db_path = "app/app.db"
migrations_path = Config.MIGRATIONS_DIR


@db_cli.command('reset', help="resets your current db config and data")
def reset_db():
    print()

    if os.path.isfile(db_path):
        print("db file found - deleting...")
        os.remove(db_path)
        print("db file deleted!\n")

    if os.path.isdir(migrations_path):
        print("migrations found - deleting...")
        shutil.rmtree(migrations_path)
        print("migrations deleted!\n")

    print("setting up the db...")
    flask_migrate.init()
    flask_migrate.migrate()
    flask_migrate.upgrade()
    print("db has been successfully setup!\n")

    print("Local setup has successfully been reset!")
