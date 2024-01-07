import os

from flask import Flask

from src.data import mongo_setup


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    mongo_setup.global_init()

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import expense
    app.register_blueprint(expense.bp)

    return app
