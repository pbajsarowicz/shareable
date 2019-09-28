import pytz
from datetime import datetime
from unittest.mock import patch, Mock

from django.test import TestCase
from parameterized import parameterized

from shareable.models import Shareable


class MockDatetime(datetime):
    def __new__(cls, *args, **kwargs):
        return datetime.__new__(datetime, *args, **kwargs)


class ShareableTestCase(TestCase):
    fixtures = ['shareable.json']

    def setUp(self):
        self.shareable_object = Shareable.objects.get(id=1)

    @parameterized.expand([
        ('valid', datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.UTC), False),
        ('expired', datetime(2000, 1, 2, 0, 0, 1, tzinfo=pytz.UTC), True),
    ])
    def test_expiration(self, name, now_datetime, expected):
        with patch('shareable.models.timezone') as mock_method:
            mock_method.now.return_value = now_datetime
            self.assertEqual(self.shareable_object.is_expired, expected)
