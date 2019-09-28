from datetime import datetime
from unittest.mock import Mock

from django.test import TestCase

from shareable.views import ShareableDetailView


class MockDatetime(datetime):
    def __new__(cls, *args, **kwargs):
        return datetime.__new__(datetime, *args, **kwargs)


class ShareableDetailViewTestCase(TestCase):

    def test_expiration(self):
        mock_request = Mock()
        view = ShareableDetailView(request=mock_request)

        view.shareable_object = Mock(is_expired=True)
        self.assertTrue('error_message' in view.get_context_data())
        self.assertEqual(
            view.get_context_data()['error_message'], 'The link has expired'
        )

        view.shareable_object = Mock(is_expired=False)
        self.assertFalse('error_message' in view.get_context_data())
