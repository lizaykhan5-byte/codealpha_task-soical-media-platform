from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Notification
from accounts.models import FollowRequest


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    follow_requests = FollowRequest.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    notifications.update(is_read=True)

    return render(request, "notifications/notifications.html", {
        "notifications": notifications,
        "follow_requests": follow_requests,
    })