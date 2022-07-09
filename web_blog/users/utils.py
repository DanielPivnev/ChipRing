import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from web_blog import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Запрос на сброс пароля',
                  sender='...',
                  recipients=[user.email])
    msg.body = f'Чтобы сбросить пароль, перейдите по следующей ссылке: ' \
               f'{url_for("users.reset_token", token=token, _external=True)}. ' \
               f'Если вы не делали этот запрос тогда просто проигнорируйте это ' \
               f'письмо и никаких изменений не будет.'

    mail.send(msg)


def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static/profile_pics', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
