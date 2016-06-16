# flake8: ignore=E402
import sys

from flask.ext.script import Manager
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "flixbus"))
from app import create_app, db  # NOQA

# Need to import all the models here in order for them to be synced
from flixbus.models.common import *  # NOQA

app = create_app()
manager = Manager(app)


@manager.command
def syncdb():
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == "__main__":
    manager.run()
