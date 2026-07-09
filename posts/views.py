from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from notifications.models import Notification
from stories.models import Story
from .models import Post
from .forms import PostForm, CommentForm


@login_required
def home(request):
    if request.user.is_authenticated:
        following_users = request.user.profile.following.all()
        feed_users = list(following_users) + [request.user]

        posts = Post.objects.filter(author__in=feed_users).order_by("-created_at")

        my_story = Story.objects.filter(
            user=request.user,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by("-created_at").first()

        stories = Story.objects.filter(
            user__in=following_users,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by("-created_at")

    else:
        posts = Post.objects.none()
        my_story = None
        stories = Story.objects.none()

    comment_form = CommentForm()

    return render(request, "posts/home.html", {
        "posts": posts,
        "stories": stories,
        "my_story": my_story,
        "comment_form": comment_form,
    })


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm()

    return render(request, "posts/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
    })


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

        if post.author != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                post=post,
                notification_type="like"
            )

    return JsonResponse({
        "liked": liked,
        "total_likes": post.total_likes()
    })


@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.saved_by.all():
        post.saved_by.remove(request.user)
        saved = False
    else:
        post.saved_by.add(request.user)
        saved = True

    return JsonResponse({
        "saved": saved,
        "total_saves": post.total_saves()
    })


@login_required
def saved_posts(request):
    posts = request.user.saved_posts.all().order_by("-created_at")

    return render(request, "posts/saved_posts.html", {
        "posts": posts
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            if post.author != request.user:
                Notification.objects.create(
                    sender=request.user,
                    receiver=post.author,
                    post=post,
                    notification_type="comment"
                )

    return redirect("post_detail", post_id=post.id)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit_post.html", {
        "form": form,
        "post": post
    })


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("profile")

    return render(request, "posts/delete_post.html", {
        "post": post
    })