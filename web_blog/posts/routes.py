from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from web_blog import db
from web_blog.models import Post, User
from web_blog.posts.forms import PostForm
from web_blog.users.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route('/')
@posts.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).\
        paginate(page=page, per_page=9)
    return render_template('home.html', posts=posts, flag=False)


@posts.route('/user_posts/<int:user_id>')
def user_posts(user_id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=user_id).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=9)
    return render_template('home.html', posts=posts, user=user, flag=True)


@posts.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'post_pics')
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id, image_file=picture_file)
        else:
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.home'))
    return render_template('create_post.html', title='New Post', form=form)


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    author = User.query.get_or_404(post.user_id)
    return render_template('post.html', title=post.title, post=post, author=author)


@posts.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'post_pics')
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('posts.home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)


@posts.route('/delete_post/<int:post_id>',)
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.home'))
