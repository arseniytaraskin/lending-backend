from django.urls import path
from .views import get_text_blocks

urlpatterns = [
    path('text-blocks/', get_text_blocks, name='get_text_blocks'),
]
