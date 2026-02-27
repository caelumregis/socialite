from django.db import models

from django.conf import settings
# Create your models here.


class Post(models.Model):
    # a simple user post. Text only for now

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post(id={self.id}, author_id={self.author_id})"
    
class Comment(models.Model):
    # A comment made by a user on a post
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    # A single reaction per user per post. Re-react updates the type.
    LIKE = "like"
    LOVE = "love"
    HAHA = "haha"
    SAD = "sad"
    ANGRY = "angry"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (LOVE, "Love"),
        (HAHA, "Haha"),
        (SAD, "Sad"),
        (ANGRY, "Angry"),
        ]

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reactions",
    )

    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents duplicates: one reaction per user per post
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_user_reaction_per_post")
        ]