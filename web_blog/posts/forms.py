from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Change photo',
                        validators=[
                            FileAllowed(['jpg', 'jpeg', 'png'])
                        ])
    submit = SubmitField('Save')


class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Comment')


class UsernameSearchForm(FlaskForm):
    username = StringField('Content', validators=[DataRequired()], render_kw={'placeholder': 'Username...'})
    submit = SubmitField('Search')
