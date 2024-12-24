from django.contrib import admin
from .models import TextBlock, ImageBlock, Frame, ContentBlock

# Регистрируем модель TextBlock для отображения в админ-панели
admin.site.register(TextBlock)
admin.site.register(ImageBlock)

admin.site.register(ContentBlock)

admin.site.register(Frame)

