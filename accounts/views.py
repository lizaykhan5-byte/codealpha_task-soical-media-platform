from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from notifications.models import Notification
from .models import FollowRequest
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html")

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    is_following = profile_user in request.user.profile.following.all()

    is_followed_by = request.user in profile_user.profile.following.all()

    follow_request_sent = FollowRequest.objects.filter(
        sender=request.user,
        receiver=profile_user
    ).exists()

    return render(request, "accounts/user_profile.html", {
        "profile_user": profile_user,
        "is_following": is_following,
        "is_followed_by": is_followed_by,
        "follow_request_sent": follow_request_sent,
    })


@login_required
def follow_toggle(request, username):
    profile_user = get_object_or_404(User, username=username)

    if profile_user == request.user:
        return redirect("user_profile", username=username)

    # Already following = unfollow
    if profile_user in request.user.profile.following.all():
        request.user.profile.following.remove(profile_user)

        FollowRequest.objects.filter(
            sender=request.user,
            receiver=profile_user
        ).delete()

        Notification.objects.filter(
            sender=request.user,
            receiver=profile_user,
            notification_type="follow"
        ).delete()

        return redirect("user_profile", username=username)

    # If request already sent, do nothing
    if FollowRequest.objects.filter(
        sender=request.user,
        receiver=profile_user
    ).exists():
        return redirect("user_profile", username=username)

    # Create follow request
    FollowRequest.objects.create(
        sender=request.user,
        receiver=profile_user
    )

    Notification.objects.create(
        sender=request.user,
        receiver=profile_user,
        notification_type="follow"
    )

    return redirect("user_profile", username=username)

@login_required
def accept_follow_request(request, request_id):
    follow_request = get_object_or_404(
        FollowRequest,
        id=request_id,
        receiver=request.user
    )

    follow_request.sender.profile.following.add(request.user)

    Notification.objects.filter(
        sender=follow_request.sender,
        receiver=request.user,
        notification_type="follow"
    ).delete()

    follow_request.delete()

    return redirect("notifications")


@login_required
def reject_follow_request(request, request_id):
    follow_request = get_object_or_404(
        FollowRequest,
        id=request_id,
        receiver=request.user
    )

    Notification.objects.filter(
        sender=follow_request.sender,
        receiver=request.user,
        notification_type="follow"
    ).delete()

    follow_request.delete()

    return redirect("notifications")

@login_required
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "accounts/edit_profile.html", {
        "u_form": u_form,
        "p_form": p_form
    })


@login_required
def search_users(request):
    query = request.GET.get("q")
    users = []

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(
            id=request.user.id
        )

    return render(request, "accounts/search.html", {
        "query": query,
        "users": users
    })

@login_required
def followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)

    can_view = (
        profile_user == request.user or
        profile_user in request.user.profile.following.all()
    )

    if not can_view:
        return redirect("user_profile", username=username)

    followers = profile_user.followers.select_related("user")

    return render(request, "accounts/followers_list.html", {
        "profile_user": profile_user,
        "followers": followers
    })


@login_required
def following_list(request, username):
    profile_user = get_object_or_404(User, username=username)

    can_view = (
        profile_user == request.user or
        profile_user in request.user.profile.following.all()
    )

    if not can_view:
        return redirect("user_profile", username=username)

    following = profile_user.profile.following.all()

    return render(request, "accounts/following_list.html", {
        "profile_user": profile_user,
        "following": following
    })
