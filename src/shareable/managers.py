from django.db import models
from django.db.models import functions


class ShareableManager(models.Manager):

    def get_files(self):
        return super().get_queryset().filter(url__isnull=True)

    def get_urls(self):
        return super().get_queryset().filter(file__isnull=True)

    def get_report(self):
        return super().get_queryset().filter(
            views_counter__gte=1
        ).annotate(
            date=functions.TruncDate('created_at'),
        ).values(
            'date', 'shareable_type'
        ).annotate(
            count=models.Count('*')
        ).order_by('date')
