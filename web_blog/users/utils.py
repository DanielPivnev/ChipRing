import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from web_blog import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Запрос на сброс пароля',
                  sender='danpivnev@yandex.ru',
                  recipients=[user.email])
    msg.body = f'''Чтобы сбросить пароль,
     перейдите по следующей ссылке: {url_for('users.reset_token',
                                       token=token, _external=True)}. Если
                                        вы не делали этот запрос
                                        тогда просто проигнорируйте это письмо
                                        и никаких изменений не будет.'''
    mail.send(msg)


def save_picture(form_picture, folder, x_size=150, y_size=150):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                f'static/{folder}', picture_fn)

    output_size = (x_size, y_size)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
