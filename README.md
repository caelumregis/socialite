# Socialite API

A backend REST API for a simple social media platform built with Django REST Framework.

Socialite supports:

- Google OAuth login
- JWT authentication
- Post creation
- Commenting on posts
- Reacting to posts

This project is designed for backend architecture practice and professional Git workflow training.

---

## 🚀 Tech Stack

- Python 3
- Django
- Django REST Framework
- SimpleJWT
- Google OAuth (ID token verification)
- SQLite (development database)

---

## 🔐 Authentication Architecture

Socialite uses a two-step authentication flow:

1. Google OAuth authentication
2. JWT token issuance for API access

### Flow

1. Client authenticates with Google.
2. Google returns an `id_token`.
3. Client sends `id_token` to:

   POST `/api/auth/google/`

4. Backend verifies the Google ID token.
5. Backend issues:
   - `access` token
   - `refresh` token
6. Client uses:

   `Authorization: Bearer <access_token>`

to access protected endpoints.

---

## 🏗 Project Structure

```
socialite/
│
├── config/            # Django project configuration
├── accounts/          # Authentication logic (Google OAuth)
├── posts/             # Posts, comments, reactions
├── manage.py
└── requirements.txt
```

---

## ⚙️ Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/socialite.git
cd socialite
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run Server

```bash
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000/
```

---

## 🔑 Environment Configuration

In `config/settings.py`, configure:

```
GOOGLE_OAUTH_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
```

This is required for Google ID token verification.

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | `/api/auth/token/` | Obtain JWT via username/password |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| POST | `/api/auth/google/` | Exchange Google ID token for JWT |

---

### Posts

| Method | Endpoint | Description |
|--------|----------|------------|
| GET | `/api/posts/` | List posts |
| POST | `/api/posts/` | Create post |
| POST | `/api/posts/{id}/comment/` | Comment on post |
| POST | `/api/posts/{id}/react/` | React to post |

All endpoints require:

```
Authorization: Bearer <access_token>
```

---

## 🧠 Core Concepts Practiced

- JWT authentication
- Google OAuth ID token verification
- DRF ViewSets
- Custom DRF actions
- Serializer validation
- Database constraints
- Professional Git branching workflow

---

## 🌱 Branching Strategy

Feature-based workflow:

- `feature/<feature-name>`
- `docs/<documentation>`
- `main` for stable code

Workflow:

1. Create feature branch
2. Implement feature
3. Test via Postman
4. Merge to main
5. Delete feature branch

---

## 🔮 Future Improvements

- Nested post responses
- Reaction counts aggregation
- Author-only edit/delete permissions
- Pagination
- Follow system
- Deployment configuration
- Docker support

---

## 📚 Educational Purpose

This project is built as part of backend systems training to simulate a real-world social media API using professional development practices.