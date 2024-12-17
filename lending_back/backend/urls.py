from django.urls import path
from .views import *

urlpatterns = [
    path('text-blocks/', get_text_blocks, name='get_text_blocks'),
    path('text-blocks/add/', add_text_blocks, name='add_text_block'),
    path('text-blocks/<int:pk>/update/', update_text_blocks, name='update_text_block'),
    path('text-blocks/<int:pk>/delete/', delete_text_block, name='delete_text_block'),
    path('images/', get_images, name='get_images'),
    path('images/<int:pk>/update/', update_image, name='update_image'),
    path('images/add/', add_image, name='add_image'),
    path('images/<int:pk>/delete/', delete_image, name='delete_image'),
]
