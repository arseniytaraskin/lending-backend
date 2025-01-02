from django.urls import path
from .views import *
from .views_frame import *

urlpatterns = [

    path('text-blocks/', get_text_blocks, name='get_text_blocks'),
    path('text-blocks/add/', add_text_blocks, name='add_text_block'),
    path('text-blocks/<int:pk>/update/', update_text_blocks, name='update_text_block'),
    path('text-blocks/<int:pk>/delete/', delete_text_block, name='delete_text_block'),
    path('text-blocks/<int:pk>/', get_text_block_by_id, name='get_text_block_by_id'),
    path('images/', get_images, name='get_images'),
    path('images/<int:pk>/update/', update_image, name='update_image'),
    path('images/add/', add_image, name='add_image'),
    path('images/<int:pk>/delete/', delete_image, name='delete_image'),
    path('images/<int:pk>/', get_image_by_id, name='get_image_by_id'),

    path('content-blocks/', list_content_blocks, name='list_content_blocks'),
    path('content-blocks/<int:pk>/update/', update_content_block, name='update_content_block'),
    path('content-blocks/<int:pk>/delete/', delete_content_block, name='delete_content_block'),
    path('content-blocks/<int:pk>/', get_content_block, name='get_content_block'),
    path('content-blocks/add/', create_content_block, name='create_content_block'),

    path('frames/', get_frames, name='get_frames'),
    path('frames/add/', add_frame, name='add_frame'),
    path('frames/<int:pk>/', get_frame_by_id, name='get_frame_by_id'),
    path('frames/<int:pk>/update/', update_frame, name='update_frame'),
    path('frames/<int:pk>/delete/', delete_frame, name='delete_frame'),

    path('styles/', GetMainStylesView.as_view(), name='get_styles'),
    path('styles/add/', PostMainStyleView.as_view(), name='post_style'),
    path('styles/update/<int:pk>/', PatchMainStyleView.as_view(), name='update_style'),
    path('styles/delete/<int:pk>/', DeleteMainStyleView.as_view(), name='delete_style'),
    path('styles/<int:pk>/', GetMainStyleByIdView.as_view(), name='get_style_by_id'),

]
