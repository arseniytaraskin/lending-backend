from django.urls import path
from .views import *

app_name = "auth"

urlpatterns = [
    path('', get),
    path('create', create),
    path('update', update),
    path('delete', delete),
]
