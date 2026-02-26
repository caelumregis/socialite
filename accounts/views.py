from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Google ID token verification (server-side)
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Socialite JWT issuance
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class GoogleLoginView(APIView):
    """
    Exchanges a Google ID token for Socialite JWT tokens.
    Client sends: { "id_token": "<google_id_token>" }
    Server returns: { "access": "...", "refresh": "...", "user": {...} }
    """

    permission_classes = []  # Public endpoint (no auth required)

    def post(self, request):
        # Validate request payload
        google_id_token = request.data.get("id_token")
        if not google_id_token:
            return Response(
                {"detail": "id_token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verify token signature and audience (prevents token spoofing)
        try:
            payload = id_token.verify_oauth2_token(
                google_id_token,
                google_requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID,
            )
        except Exception as e:
            return Response(
                {"detail": "Invalid Google ID token.", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Extract identity
        email = payload.get("email")
        if not email:
            return Response(
                {"detail": "Google token does not include email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create or fetch user (minimal user model for now)
        user, _ = User.objects.get_or_create(
            username=email,
            defaults={"email": email},
        )

        # Issue Socialite JWT tokens for API access
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {"id": user.id, "email": user.email, "username": user.username},
            },
            status=status.HTTP_200_OK,
        )