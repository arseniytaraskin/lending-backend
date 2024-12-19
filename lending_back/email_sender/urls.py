from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "email_sender"

urlpatterns = [
    path('send', views.send),
]
