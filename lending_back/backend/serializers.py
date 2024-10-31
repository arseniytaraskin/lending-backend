from rest_framework import serializers
from .models import TextBlock, ImageBlock

class TextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBlock
        #fields = ['id', 'title', 'content', 'is_enabled']
        fields = ['content']

class ImageBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBlock
        fields = ['id', 'image', 'description']



