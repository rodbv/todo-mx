# core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models  # <-- NEW


class UserProfile(AbstractUser):
    pass


# NEW
class Todo(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(
        UserProfile,
        related_name="todos",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
