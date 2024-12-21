from django.db import models

# Create your models here.

from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey #
from django.contrib.contenttypes.models import ContentType #позволит мне определить тип модели во время выполнения

class Frame(models.Model):
    is_enabled = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    style = models.JSONField(blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Frame {self.id} - Enabled: {self.is_enabled}"


class TemplateBlock(models.Model): # для шаблонных блоков
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    default_content = models.JSONField()  # JSON-описание, что включает шаблон

    def __str__(self):
        return self.name




class TextBlock(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_enabled = models.BooleanField(default=True)

    # Настройки шрифта
    font_family = models.CharField(max_length=100, default="Arial")
    font_size = models.IntegerField(default=14)
    font_weight = models.CharField(max_length=50, default="normal")
    font_style = models.CharField(max_length=50, default="normal")
    color = models.CharField(max_length=7, default="#000000")  # HEX-код цвета текста


    line_height = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, default=1.5)  # Межстрочный интервал
    text_align = models.CharField(
        max_length=10,
        choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')],
        default='left'
    )  # Выравнивание текста
    list_type = models.CharField(
        max_length=10,
        choices=[('none', 'None'), ('numbered', 'Numbered'), ('bulleted', 'Bulleted')],
        default='none'
    )  # Тип списка: нумерованный или маркированный
    link = models.URLField(blank=True, null=True)  # Гиперссылка для добавления ссылок в текст

    def __str__(self):
        return self.title


class ImageBlock(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or "Image Block"


class Application(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    organization = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




