import binascii
from six import string_types
from base64 import b64decode, b64encode

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64FileField(serializers.FileField):
    ERROR_MESSAGE = 'Provided value must be a base64-encoded string.'

    @staticmethod
    def _get_cleaned_data(data):
        if ';base64,' in data:
            _, data = data.split(';base64,')
        return data

    def get_content(self, data):
        data = self._get_cleaned_data(data)

        try:
            return b64decode(data)
        except (TypeError, binascii.Error, ValueError):
            raise ValidationError(self.ERROR_MESSAGE)

    def to_internal_value(self, data):
        if data and isinstance(data, string_types):
            content = self.get_content(data)
            content_file = ContentFile(content, name='._shareable')

            return super().to_internal_value(content_file)
        raise ValidationError(self.ERROR_MESSAGE)

    def to_representation(self, value):
        if not value:
            return ''

        try:
            if isinstance(value, ContentFile):
                with value.file as file:
                    return b64encode(file.read()).decode()

            with open(value.path, 'rb') as file:
                return b64encode(file.read()).decode()
        except Exception:
            raise IOError('Error while encoding a file')
