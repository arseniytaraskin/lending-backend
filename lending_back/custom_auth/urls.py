from django.urls import path
from .views import *

app_name = "auth"

urlpatterns = [
    path('login', loginView),
    path('register', registerView),
    path('refresh', CookieTokenRefreshView.as_view()),
    path('logout', logoutView),
    path("user", user),
]
