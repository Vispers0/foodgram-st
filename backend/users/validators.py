import re  # type:ignore

from django.core.exceptions import ValidationError  # type:ignore

from .constants import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH, MAX_PASSWORD_LENGTH


def validate_username(username):
    if username.lower() == 'me':
        raise ValidationError(
            'Нельзя назвать логин "me".'
        )
    if len(username) > NAME_MAX_LENGTH:
        raise ValidationError(
            f'Длина логина не должна превышать '
            f'{NAME_MAX_LENGTH} символов.'
        )
    if not re.fullmatch(r'^[\w.@+-]+$', username):
        raise ValidationError(
            'Логин содержит недопустимые символы.'
        )
    return username


def validate_email(email):
    if len(email) > EMAIL_MAX_LENGTH:
        raise ValidationError(
            'Email слишком длинный.'
        )
    return email


class MaxLengthPasswordValidator:
    def __init__(self, max_length=MAX_PASSWORD_LENGTH):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                f'Длина пароля не должна превышать {self.max_length} символов.'
            )

    def get_help_text(self):
        return f'Длина пароля не должна превышать {self.max_length} символов.'
