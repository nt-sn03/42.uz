from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    chat_id = models.CharField(max_length=255, unique=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return self.username
    