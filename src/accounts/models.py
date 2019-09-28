from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

    def update_user_agent(self, request):
        http_user_agent = request.META.get('HTTP_USER_AGENT')

        if http_user_agent and http_user_agent != self.user_agent:
            self.user_agent = http_user_agent
            self.save()
