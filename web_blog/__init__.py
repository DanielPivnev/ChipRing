from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from web_blog.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    bcrypt.init_app(app)

    from web_blog.main.routes import main
    from web_blog.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.config.from_object(Config)

    login_manager.init_app(app)

    return app
