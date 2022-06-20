from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from web_blog.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    db.init_app(app)

    from web_blog.main.routes import main
    app.register_blueprint(main)
    app.config.from_object(Config)

    login_manager.init_app(app)

    return app
