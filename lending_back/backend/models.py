from django.db import models

# Create your models here.

from django.db import models

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
