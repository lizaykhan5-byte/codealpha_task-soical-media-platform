from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Story(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories"
    )

    image = models.ImageField(upload_to="stories/")
    caption = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    viewers = models.ManyToManyField(
        User,
        related_name="viewed_stories",
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def is_active(self):
        return self.created_at >= timezone.now() - timedelta(hours=24)

    def __str__(self):
        return f"{self.user.username} story"