from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Story
from inbox.models import Message


@login_required
def create_story(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        caption = request.POST.get("caption")

        if image:
            Story.objects.create(
                user=request.user,
                image=image,
                caption=caption
            )
            return redirect("home")

    return render(request, "stories/create_story.html")


@login_required
def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.method == "POST" and story.user != request.user:
        action = request.POST.get("action")

        if action == "reply":
            reply = request.POST.get("reply")
            if reply:
                Message.objects.create(
                    sender=request.user,
                    receiver=story.user,
                    body=f"💬 Replied to your story: {reply}"
                )

        elif action == "react":
            emoji = request.POST.get("emoji", "❤️")
            Message.objects.create(
                sender=request.user,
                receiver=story.user,
                body=f"{emoji} reacted to your story"
            )

        return redirect("story_detail", story_id=story.id)

    if story.user != request.user:
        story.viewers.add(request.user)

    active_stories = Story.objects.filter(
        user=story.user,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by("created_at")

    story_ids = list(active_stories.values_list("id", flat=True))
    current_index = story_ids.index(story.id)

    previous_story = active_stories[current_index - 1] if current_index > 0 else None
    next_story = active_stories[current_index + 1] if current_index < len(story_ids) - 1 else None

    return render(request, "stories/story_detail.html", {
        "story": story,
        "active_stories": active_stories,
        "previous_story": previous_story,
        "next_story": next_story,
        "viewers": story.viewers.all(),
    })


@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, user=request.user)
    story.delete()
    return redirect("home")