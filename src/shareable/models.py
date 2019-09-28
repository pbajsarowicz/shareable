import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import User
from shareable.const import ShareableTypes
from shareable.fields import HashField
from shareable.managers import ShareableManager
from shareable.utils import get_expired_at


class Shareable(models.Model):
    SHAREABLE_TYPES = (
        (ShareableTypes.FILE, ShareableTypes.FILE),
        (ShareableTypes.URL, ShareableTypes.URL)
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    password = HashField()
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='shareables', null=True
    )
    url = models.URLField(null=True, blank=True)
    shareable_type = models.CharField(choices=SHAREABLE_TYPES, max_length=16)
    file = models.FileField(
        null=True, blank=True, upload_to=settings.FILES_DIR
    )
    views_counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField(default=get_expired_at)

    objects = ShareableManager()

    @property
    def is_expired(self):
        return timezone.now() > self.expired_at

    def save(self, *args, **kwargs):
        if not self.shareable_type:
            self.shareable_type = (
                ShareableTypes.FILE if self.url is None else ShareableTypes.URL
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        indexes = [
            models.Index(
                fields=('shareable_type', 'user'),
                name='shareable_type_user_idx'
            ),
            models.Index(fields=('uuid',), name='uuid_idx'),
        ]
