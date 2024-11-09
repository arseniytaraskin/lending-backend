from rest_framework import serializers
from .models import TextBlock, ImageBlock

class TextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBlock
        #fields = ['id', 'title', 'content', 'is_enabled']
        #fields = ['content']

        fields = [
            'id', 'title', 'content', 'is_enabled',
            'font_family', 'font_size', 'font_weight', 'font_style', 'color',
            'line_height', 'text_align', 'list_type', 'link'
        ]

class ImageBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBlock
        fields = ['id', 'image', 'description']



