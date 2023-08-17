from django.conf.global_settings import FILE_UPLOAD_HANDLERS
from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('Value must contain only letters')


