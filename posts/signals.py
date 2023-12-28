from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from posts.models import Post
from notifications.models import Notification


@receiver(m2m_changed, sender="user_profile.UserProfile_liked_posts")
def like_handler(sender, **kwargs):
    user_profile = kwargs.pop("instance")
    action = kwargs.pop("action")
    pk_set = kwargs.pop("pk_set")
    if not pk_set:
        return
    (post_id,) = pk_set
    post = Post.objects.get(id=post_id)

    if action == "post_add":  # Like
        Notification.objects.create(
            issuer=user_profile, post=post, receiver=post.user, notification_type="L"
        )

    elif action == "post_remove":
        like_notification = Notification.objects.filter(
            issuer=post.user, post=post, receiver=user_profile, notification_type="L"
        )
        like_notification.exists() and like_notification[0].delete()
    ...


@receiver(post_save, sender="posts.Post")
def repost_creation_handler(sender, **kwargs):
    post = kwargs.pop("instance")
    if not post.repost:
        return

    print("instance", post)

    Notification.objects.create(
        issuer=post.user,
        post=post.embed,
        receiver=post.embed.user,
        notification_type="T",
    )


@receiver(post_delete, sender="posts.Post")
def repost_deletion_handler(sender, **kwargs):
    post = kwargs.pop("instance")
    if not post.repost:
        return

    print("delete post", post)

    notification = Notification.objects.filter(
        issuer=post.user,
        post=post.embed,
        receiver=post.embed.user,
        notification_type="T",
    )

    notification.exists() and notification[0].delete()


@receiver(post_save, sender="posts.Post")
def reply_creation_handler(sender, **kwargs):
    post = kwargs.pop("instance")
    if not post.reply_to:
        return

    Notification.objects.create(
        issuer=post.user,
        post=post.reply_to,
        receiver=post.reply_to.user,
        notification_type="R",
    )

    print(
        f"{post.user} replied to {post.reply_to.text} you are {post.reply_to.user}",
        post,
    )


@receiver(post_delete, sender="posts.Post")
def reply_deletion_handler(sender, **kwargs):
    post = kwargs.pop("instance")
    if not post.reply_to:
        return

    notification = Notification.objects.filter(
        issuer=post.user,
        post=post.reply_to,
        receiver=post.reply_to.user,
        notification_type="R",
    )

    notification.exists() and notification.delete()


@receiver(post_save, sender="user_profile.Mention")
def mention_handler(sender, **kwargs):
    mention = kwargs.pop("instance")
    Notification.objects.create(
        issuer=mention.post.user,
        post=mention.post,
        receiver=mention.user_profile,
        notification_type="M",
    )
    print("mentioned user", mention.user_profile)
    print("mentioned post", mention.post.text)
