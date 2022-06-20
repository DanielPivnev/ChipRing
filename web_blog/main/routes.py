from flask import render_template, Blueprint

from web_blog.models import User

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')
