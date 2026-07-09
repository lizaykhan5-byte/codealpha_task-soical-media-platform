from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Message


@login_required
def inbox_home(request):
    query = request.GET.get("q", "")

    users = request.user.profile.following.all()
    

    if query:
        users = users.filter(username__icontains=query)

    conversations = []

    for u in users:
        

        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=u) |
            Q(sender=u, receiver=request.user)
        ).order_by("-created_at").first()

        unread_count = Message.objects.filter(
            sender=u,
            receiver=request.user,
            is_read=False
        ).count()

        conversations.append({
            "username": u.username,
            "profile_picture": u.profile.profile_picture if hasattr(u, "profile") else None,
            "is_online": u.profile.is_online if hasattr(u, "profile") else False,
            "last_message": last_message,
            "unread_count": unread_count,
        })

    return render(request, "inbox/inbox.html", {
        "conversations": conversations,
        "query": query,
    })


@login_required
def chat_room(request, username):
    receiver = get_object_or_404(User, username=username)

    if receiver not in request.user.profile.following.all():
        return redirect("inbox")

    is_blocked_by_me = receiver in request.user.profile.blocked_users.all()
    has_blocked_me = request.user in receiver.profile.blocked_users.all()

    if request.method == "POST" and not is_blocked_by_me and not has_blocked_me:
        body = request.POST.get("body", "")
        image = request.FILES.get("image")

        if body or image:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                body=body,
                image=image
            )

        return redirect("chat_room", username=receiver.username)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by("created_at")

    Message.objects.filter(
        sender=receiver,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return render(request, "inbox/chat_room.html", {
        "receiver": receiver,
        "messages": messages,
        "is_blocked_by_me": is_blocked_by_me,
        "has_blocked_me": has_blocked_me,
    })


@login_required
def delete_chat(request, username):
    other_user = get_object_or_404(User, username=username)

    Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).delete()

    return redirect("inbox")


@login_required
def block_user(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user != request.user:
        request.user.profile.blocked_users.add(other_user)

    return redirect("inbox")


@login_required
def unblock_user(request, username):
    other_user = get_object_or_404(User, username=username)

    request.user.profile.blocked_users.remove(other_user)

    return redirect("chat_room", username=username)