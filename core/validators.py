import os

from django.core.exceptions import ValidationError


def csv_file_validator(value):
    filename, ext = os.path.splitext(value.name)
    if str(ext) != '.csv':
        raise ValidationError("A extensão do arquivo deve ser .csv.")
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('O tamanho do arquivo não pode exceder 1 mb.')
    return True
