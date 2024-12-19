from django.urls import path
from .views import *

app_name = "auth"

urlpatterns = [
    path('login', loginView),
    path('refresh', CookieTokenRefreshView.as_view()),
    path('logout', logoutView),
    path("user", user),
    path("admin", admin),
    path("staff", staff),
    path("superuser", superuser),
]
