from flask import (render_template, url_for,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from web_blog import db
from web_blog.models import Post, User, Comment
from web_blog.posts.forms import PostForm, CommentForm, UsernameSearchForm
from web_blog.users.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route('/', methods=['GET', 'POST'])
@posts.route('/home/', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()). \
        paginate(page=page, per_page=6)

    form = UsernameSearchForm()
    if form.validate_on_submit() or request.args.get('username'):
        username = form.username.data if form.validate_on_submit() else request.args.get('username')
        users = User.query.filter(User.username.contains(username))
        users_id = [user.id for user in users]
        posts = Post.query.filter(Post.user_id.in_(users_id)) \
            .order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
        parameters = f'&username={username}'
        form.username.data = username

        return render_template('posts/home.html', posts=posts, flag=False, form=form, parameters=parameters)

    return render_template('posts/home.html', posts=posts, flag=False, form=form, parameters='')


@posts.route('/user_posts/<int:user_id>/', methods=['GET', 'POST'])
def user_posts(user_id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=user_id).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=6)

    form = UsernameSearchForm()
    if form.validate_on_submit():
        username = form.username.data

        return redirect(f'{url_for("posts.home")}?username={username}')

    return render_template('posts/home.html', posts=posts, user=user, flag=True, form=form)


@posts.route('/new_post/', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'post_pics', 2000, 2000)
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id, image_file=picture_file)
        else:
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.home'))
    return render_template('posts/create_post.html', title='New Post', form=form)


@posts.route('/post/<int:post_id>/', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    author = User.query.get_or_404(post.user_id)
    context = {}

    if current_user.is_authenticated:
        comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.created_at.desc()).all()

        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(content=form.content.data,
                              user_id=current_user.id,
                              post_id=post.id)
            db.session.add(comment)
            db.session.commit()

            return redirect(url_for('posts.post', post_id=post.id))

        context['comments'] = comments
        context['form'] = form

    context['post'] = post
    context['author'] = author
    context['title'] = post.title

    return render_template('posts/post.html', **context)


@posts.route('/update_post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'post_pics', 2000, 2000)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('posts.home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts/create_post.html', title='Update Post', form=form)


@posts.route('/delete_post/<int:post_id>/', )
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.home'))
