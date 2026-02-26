from django.urls import path
from .views import GoogleLoginView

urlpatterns = [
    # exchange google id token for socialite JWT token
    path('google/', GoogleLoginView.as_view(), name='google_login'),
]