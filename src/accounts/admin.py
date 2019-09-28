from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


class AccountsUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Tracking data', {'fields': ('user_agent',)}),
    )
    readonly_fields = ('user_agent',)


admin.site.register(User, AccountsUserAdmin)
