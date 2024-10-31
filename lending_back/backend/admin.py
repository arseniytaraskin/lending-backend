from django.contrib import admin
from .models import TextBlock, ImageBlock

# Регистрируем модель TextBlock для отображения в админ-панели
admin.site.register(TextBlock)
admin.site.register(ImageBlock)
