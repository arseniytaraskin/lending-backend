from rest_framework import serializers
from .models import TextBlock, ImageBlock, Frame, ContentBlock

class TextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBlock
        fields = ['id', 'title', 'content', 'is_enabled', 'styles']

class ImageBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageBlock
        fields = ['id', 'image', 'description']


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class FrameSerializer(serializers.ModelSerializer):
    block_type = serializers.CharField(write_only=True)  # Передача типа блока, 'textblock' или 'imageblock'
    block_data = serializers.JSONField(write_only=True)  # Данные для связанного объекта


    block = serializers.SerializerMethodField()

    class Meta:
        model = Frame
        fields = ['id', 'is_enabled', 'order', 'style', 'block_type', 'block_data', 'block']

    def get_block(self, obj):
        if obj.content_type.model == 'textblock':
            from .serializers import TextBlockSerializer
            return TextBlockSerializer(obj.content_object).data
        elif obj.content_type.model == 'imageblock':
            from .serializers import ImageBlockSerializer
            return ImageBlockSerializer(obj.content_object).data
        return None

    def create(self, validated_data):
        block_type = validated_data.pop('block_type')
        block_data = validated_data.pop('block_data')


        if block_type == 'textblock':
            from .models import TextBlock
            block = TextBlock.objects.create(**block_data)
        elif block_type == 'imageblock':
            from .models import ImageBlock
            block = ImageBlock.objects.create(**block_data)
        else:
            raise serializers.ValidationError("Unsupported block type")


        frame = Frame.objects.create(
            **validated_data,
            content_type=ContentType.objects.get(model=block_type),
            object_id=block.id
        )
        return frame




class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ['id', 'name', 'enabled', 'order', 'content']
