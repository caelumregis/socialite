from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment, Reaction
from .serializers import (
    PostSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    ReactionSerializer,
    ReactionCreateSerializer,
)

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    """ CRUD for posts + custom actions for comments and reactions """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # newest posts first
        return Post.objects.select_related("author").order_by("-created_at")
    
    def perform_create(self, serializer):
        # server set author based on logged in user
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):
        """ POST /api/posts/{id}/comment/ -> create a comment on this post """
        post = self.get_object()

        payload = CommentCreateSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=payload.validated_data["content"],
        )
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )
    
    @action(detail=True, methods=["post"])
    def react(self, request, pk=None):
        """ POST /api/posts/{id}/react/ -> create/update a reaction on this post """
        post = self.get_object()

        payload = ReactionCreateSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        reaction_type = payload.validated_data["reaction_type"]

        # update or create a reaction (one per user per post)
        reaction, created = Reaction.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={"reaction_type": reaction_type},
        )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(
            ReactionSerializer(reaction).data,
            status=status_code,
        )
