from django.contrib import admin
from shareable.models import Shareable


@admin.register(Shareable)
class ShareableModelAdmin(admin.ModelAdmin):
    fields = (
        'shareable_type',
        'uuid',
        'password',
        'user',
        'url',
        'file',
        'views_counter',
        'created_at',
        'expired_at',
    )
    list_display = ('uuid', 'user', 'created_at', 'expired_at')
    list_filter = ('user', 'created_at', 'expired_at')
    readonly_fields = ('shareable_type', 'uuid', 'created_at', 'views_counter')
