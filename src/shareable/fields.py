import hashlib

from django.db import models
from django.conf import settings


class HashField(models.CharField):
    SALT = settings.HASH_FIELD_SALT

    @classmethod
    def make_hash(cls, value):
        value = (cls.SALT + value.upper().strip()).encode('utf-8')
        return hashlib.sha512(value).hexdigest()

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(HashField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if not value:
            return value

        hashed = self.make_hash(value)
        if len(value) == len(hashed):
            return value
        else:
            return hashed

    def deconstruct(self):
        name, path, args, kwargs = super(HashField, self).deconstruct()

        return name, path, args, kwargs
