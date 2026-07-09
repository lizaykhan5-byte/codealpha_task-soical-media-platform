from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='default.png'
    )

    cover_photo = models.ImageField(
        upload_to='cover_photos/',
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True, max_length=300)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    is_online = models.BooleanField(default=False)
    following = models.ManyToManyField(
        User,
        related_name='followers',
        blank=True
    )
    blocked_users = models.ManyToManyField(
    User,
    related_name="blocked_by",
    blank=True
)

    def __str__(self):
        return self.user.username


class FollowRequest(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_follow_requests"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_follow_requests"
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"