from django.contrib import admin
from .models import TextBlock

# Регистрируем модель TextBlock для отображения в админ-панели
admin.site.register(TextBlock)
