# core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    pass


class Todo(models.Model):
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(
        UserProfile,
        related_name="todos",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
