from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from web_blog.admin import AdminView
from web_blog.config import Config

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def create_app():
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from web_blog.users.routes import users
    from web_blog.posts.routes import posts
    from web_blog.admin.routes import admin_bp
    from web_blog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(admin_bp, url_prefix='/admin/')
    app.register_blueprint(errors)

    from web_blog.models import User, Post, Comment, Like, Dislike

    administration = Admin(app, name='WebBlog', index_view=AdminView(User, db.session, url='/admin/', endpoint='admin'))
    administration.add_view(AdminView(Post, db.session))
    administration.add_view(AdminView(Comment, db.session))
    administration.add_view(AdminView(Like, db.session))
    administration.add_view(AdminView(Dislike, db.session))

    return app
