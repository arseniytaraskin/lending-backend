from django.db import models

# Create your models here.

class TextBlock(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ImageBlock(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or "Image Block"
