from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from datetime import datetime, timedelta

from .models import Post, Category


@shared_task
def send_message(preview, pk, title, subscribers):
    html_content = render_to_string(
        "post_created_email.html",
        {
            "text": preview,
            "link": f"{settings.SITE_URL}/news/{pk}"
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def my_job():
    today = datetime.utcnow()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list("postCategory__name", flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list("subscribers__email", flat=True))
    print(subscribers)
    html_content = render_to_string(
        "daily_post.html",
        {
            "link": settings.SITE_URL,
            "posts": posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject="Публикации за неделю",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
