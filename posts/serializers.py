from rest_framework import serializers
from .models import Post, Comment, Reaction


class PostSerializer(serializers.ModelSerializer):
    # Read-only: author is always derived from request.user
    author_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author_id", "content", "created_at"]


class CommentCreateSerializer(serializers.Serializer):
    # Payload validator for creating a comment
    content = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post_id", "author_id", "content", "created_at"]


class ReactionCreateSerializer(serializers.Serializer):
    # Payload validator for reacting to a post
    reaction_type = serializers.ChoiceField(choices=Reaction.REACTION_CHOICES)


class ReactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reaction
        fields = ["id", "post_id", "user_id", "reaction_type", "created_at"]