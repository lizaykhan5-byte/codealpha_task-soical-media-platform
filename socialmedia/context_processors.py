from notifications.models import Notification
from inbox.models import Message


def notification_count(request):

    unread_notifications = 0
    unread_messages = 0

    if request.user.is_authenticated:

        unread_notifications = Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()

        unread_messages = Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()

    return {
        "unread_notifications": unread_notifications,
        "unread_messages": unread_messages,
    }