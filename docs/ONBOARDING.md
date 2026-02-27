# Socialite Backend – Developer Onboarding Guide

This guide will help you set up and run the Socialite backend API on your own device.

No prior Django experience required.

---

# 📌 What This Project Does

Socialite is a simple backend API that supports:

- Google OAuth login
- JWT authentication
- Create posts
- Comment on posts
- React to posts

All testing is done using Postman.

---

# 🧰 Requirements

Install these first:

- Python 3.10 or higher
- Git
- Postman
- A Google account

---

# 1️⃣ Clone the Project

Open terminal:

```bash
git clone https://github.com/YOUR_USERNAME/socialite.git
cd socialite
```

---

# 2️⃣ Create Virtual Environment

### Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

You should now see `(venv)` in your terminal.

---

# 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# 4️⃣ Configure Google OAuth

You must create a Google OAuth Client ID.

## Step 4.1 – Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Create new project named: `Socialite`

---

## Step 4.2 – Configure OAuth Consent Screen

1. APIs & Services → OAuth Consent Screen
2. Choose **External**
3. App Name: `Socialite`
4. Add your Gmail as Developer Contact
5. Add Scopes:
   - openid
   - userinfo.email
   - userinfo.profile
6. Add yourself as Test User
7. Save

---

## Step 4.3 – Create OAuth Client ID

1. APIs & Services → Credentials
2. Create Credentials → OAuth Client ID
3. Application Type: **Web Application**
4. Add Authorized Redirect URI:

```
https://developers.google.com/oauthplayground
```

5. Create

Copy:
- Client ID
- Client Secret

---

# 5️⃣ Add Client ID to Django Settings

Open file:

```
config/settings.py
```

Add this line:

```python
GOOGLE_OAUTH_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
```

Replace with your real Client ID.

---

# 6️⃣ Apply Database Migrations

```bash
python manage.py migrate
```

This creates the local SQLite database.

---

# 7️⃣ Run the Server

```bash
python manage.py runserver
```

You should see:

```
Starting development server at http://127.0.0.1:8000/
```

---

# 8️⃣ Testing Authentication in Postman

---

## Option A – Username/Password JWT Login

Create a test user:

```bash
python manage.py createsuperuser
```

Then in Postman:

### POST
```
http://127.0.0.1:8000/api/auth/token/
```

Body (JSON):

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:

```json
{
  "refresh": "...",
  "access": "..."
}
```

Save the `access` token.

---

## Option B – Google OAuth Login (Recommended)

---

### Step 1 – Get Google ID Token

Go to:

https://developers.google.com/oauthplayground

1. Click gear icon ⚙️
2. Check “Use your own OAuth credentials”
3. Paste your Client ID and Client Secret
4. Add scopes:
   - openid
   - email
   - profile
5. Authorize
6. Exchange code
7. Copy the `id_token`

IMPORTANT:
- `id_token` starts with `eyJ...`
- DO NOT use `access_token` (starts with `ya29...`)

---

### Step 2 – Exchange Google ID Token

In Postman:

POST
```
http://127.0.0.1:8000/api/auth/google/
```

Body:

```json
{
  "id_token": "PASTE_EYJ_TOKEN_HERE"
}
```

Response:

```json
{
  "access": "...",
  "refresh": "...",
  "user": {
    "id": 1,
    "email": "...",
    "username": "..."
  }
}
```

Save the Socialite `access` token.

---

# 9️⃣ Using Protected Endpoints

In Postman:

Go to Authorization tab  
Choose: Bearer Token  
Paste Socialite `access` token  

Now you can access protected APIs.

---

# 🔹 Create a Post

POST
```
http://127.0.0.1:8000/api/posts/
```

Body:

```json
{
  "content": "Hello Socialite!"
}
```

---

# 🔹 List Posts

GET
```
http://127.0.0.1:8000/api/posts/
```

---

# 🔹 Comment on a Post

POST
```
http://127.0.0.1:8000/api/posts/1/comment/
```

Body:

```json
{
  "content": "Nice post!"
}
```

---

# 🔹 React to a Post

POST
```
http://127.0.0.1:8000/api/posts/1/react/
```

Body:

```json
{
  "reaction_type": "like"
}
```

Available reactions:
- like
- love
- haha
- sad
- angry

If you react again, it updates your previous reaction.

---

# 📂 Important Files in This Project

## Authentication

```
accounts/views.py
accounts/urls.py
```

## Social Media Logic

```
posts/models.py
posts/serializers.py
posts/views.py
posts/urls.py
```

## Main Configuration

```
config/settings.py
config/urls.py
```

---

# 🚨 Common Errors

### ❌ Invalid Google ID Token
- Make sure you send `id_token`
- Ensure Client ID in settings matches Google Cloud

### ❌ 401 Unauthorized
- Make sure Bearer token is set in Postman

### ❌ ImportError: requests not installed
Run:
```bash
pip install requests
```

---

# 🎓 You Have Successfully Set Up Socialite

If all endpoints work:
- Authentication works
- Posts work
- Comments work
- Reactions work

---

# Appendix – Key Files (Reference)

This section shows the important files that make Socialite work.
If your teammate’s setup is not working, compare their files to these.

> Note: Paths are relative to the project root (same folder as `manage.py`).

---

## 1) `config/settings.py` (important parts only)

Make sure these exist:

```python
INSTALLED_APPS = [
    # Django default apps...
    "rest_framework",
    "accounts",
    "posts",
]

REST_FRAMEWORK = {
    # Read JWT token from: Authorization: Bearer <token>
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # All endpoints require login unless explicitly allowed
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# Google OAuth client id used to validate Google ID tokens
GOOGLE_OAUTH_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
```

---

## 2) `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

# SimpleJWT endpoints
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT login endpoints (username/password)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Google OAuth exchange endpoint
    path("api/auth/", include("accounts.urls")),

    # Posts endpoints
    path("api/", include("posts.urls")),
]
```

---

## 3) `accounts/urls.py`

```python
from django.urls import path
from .views import GoogleLoginView

urlpatterns = [
    # Exchange Google ID token for Socialite JWT tokens
    path("google/", GoogleLoginView.as_view(), name="google_login"),
]
```

---

## 4) `accounts/views.py`

```python
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
    Exchange a Google ID token for Socialite JWT tokens.

    Client sends:
      { "id_token": "<google_id_token>" }

    Server returns:
      { "access": "...", "refresh": "...", "user": {...} }
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

        # Verify token signature + audience (prevents spoofed tokens)
        try:
            payload = id_token.verify_oauth2_token(
                google_id_token,
                google_requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID,
            )
        except Exception:
            return Response(
                {"detail": "Invalid Google ID token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Extract identity
        email = payload.get("email")
        if not email:
            return Response(
                {"detail": "Google token does not include email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create or fetch user (minimal setup: username = email)
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
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                },
            },
            status=status.HTTP_200_OK,
        )
```

---

## 5) `posts/models.py`

```python
from django.conf import settings
from django.db import models


class Post(models.Model):
    """A simple user post (text-only)."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """A comment made by a user on a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Reaction(models.Model):
    """One reaction per user per post. Re-react updates the reaction type."""

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

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicates: a user can only have one reaction per post
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_user_reaction_per_post")
        ]
```

---

## 6) `posts/serializers.py`

```python
from rest_framework import serializers
from .models import Post, Comment, Reaction


class PostSerializer(serializers.ModelSerializer):
    """Serializer for creating/listing posts."""

    author_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author_id", "content", "created_at"]


class CommentCreateSerializer(serializers.Serializer):
    """Validates comment creation payload."""

    content = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for returning comment data."""

    author_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post_id", "author_id", "content", "created_at"]


class ReactionCreateSerializer(serializers.Serializer):
    """Validates reaction payload."""

    reaction_type = serializers.ChoiceField(choices=Reaction.REACTION_CHOICES)


class ReactionSerializer(serializers.ModelSerializer):
    """Serializer for returning reaction data."""

    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reaction
        fields = ["id", "post_id", "user_id", "reaction_type", "created_at"]
```

---

## 7) `posts/views.py`

```python
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment, Reaction
from .serializers import (
    PostSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    ReactionCreateSerializer,
    ReactionSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """CRUD for posts + custom actions for comments and reactions."""

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # Newest posts first
        return Post.objects.select_related("author").order_by("-created_at")

    def perform_create(self, serializer):
        # Server controls author: always the logged-in user
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):
        """Create a comment on a post."""
        post = self.get_object()

        payload = CommentCreateSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=payload.validated_data["content"],
        )

        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def react(self, request, pk=None):
        """Set or update the user's reaction on a post."""
        post = self.get_object()

        payload = ReactionCreateSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        reaction, created = Reaction.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={"reaction_type": payload.validated_data["reaction_type"]},
        )

        return Response(
            ReactionSerializer(reaction).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
```

---

## 8) `posts/urls.py`

```python
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")

urlpatterns = router.urls
```

---

You are fully onboarded