from django.urls import path
from .views import *

urlpatterns = [
    path('text-blocks/', get_text_blocks, name='get_text_blocks'),
    path('text-blocks/add/', add_text_blocks, name='add_text_block'),
    path('text-blocks/<int:pk>/update/', update_text_blocks, name='update_text_block')
]
