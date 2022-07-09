from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from flask_login import current_user

from web_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username:',
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    email = StringField('Email:',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField('Password:',
                             validators=[
                                 DataRequired()
                             ])
    confirm_password = PasswordField('Password (again):',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')
                                     ])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Это имя занято. Пожалуйста, выберите другое.')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Этот email занят. Пожалуйста, выберите другой.')


class LoginForm(FlaskForm):
    email = StringField('Email:',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField('Password:',
                             validators=[
                                 DataRequired()
                             ])
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    picture = FileField('Change photo',
                        validators=[
                            FileAllowed(['jpg', 'png'])
                        ])
    submit = SubmitField('Save')

    @staticmethod
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Это имя занято. Пожалуйста, выберите другой')

    @staticmethod
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email занят'
                                      'Пожалуйста, выберите другой')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    submit = SubmitField('Change Password')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'Аккаунт с данным email-адресом отсутствует. Вы можете зарегистрировать его')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль:',
                             validators=[
                                 DataRequired()
                             ])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')
                                     ])
    submit = SubmitField('Save New Password')
