from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from accounts.models import User


def generate_password():
    return User.objects.make_random_password(10)


def get_expired_at():
    return (
        timezone.now() + timedelta(hours=settings.SHAREABLE_EXPIRATION_HOURS)
    )
