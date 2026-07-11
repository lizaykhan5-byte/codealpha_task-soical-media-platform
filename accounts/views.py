from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.urls import reverse

from notifications.models import Notification
from .models import FollowRequest
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = signing.dumps(
                {"user_id": user.pk},
                salt="email-verification"
            )

            verification_url = request.build_absolute_uri(
                reverse(
                    "verify_email",
                    kwargs={"token": token}
                )
            )

            send_mail(
                subject="Verify your SocialHub account",
                message=(
                    f"Hello @{user.username},\n\n"
                    "Click the link below to verify your SocialHub account:\n\n"
                    f"{verification_url}\n\n"
                    "This verification link expires in 24 hours."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "Account created. Check your email to verify your account."
            )

            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )

def verify_email(request, token):
    try:
        data = signing.loads(
            token,
            salt="email-verification",
            max_age=60 * 60 * 24
        )

        user = get_object_or_404(
            User,
            pk=data["user_id"]
        )

    except signing.SignatureExpired:
        messages.error(
            request,
            "Verification link has expired."
        )
        return redirect("login")

    except signing.BadSignature:
        messages.error(
            request,
            "Invalid verification link."
        )
        return redirect("login")

    if not user.is_active:
        user.is_active = True
        user.save(update_fields=["is_active"])

        messages.success(
            request,
            "Email verified successfully. You can now log in."
        )
    else:
        messages.info(
            request,
            "Your email is already verified."
        )

    return redirect("login")

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
