from rest_framework import serializers
from .models import TextBlock

class TextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBlock
        #fields = ['id', 'title', 'content', 'is_enabled']
        fields = ['content']


