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
    styles = models.JSONField(default=dict)  # Хранит все стили как JSON

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




