from rest_framework import serializers


class Letter(serializers.Serializer):
    recipient = serializers.EmailField()
    sender = serializers.CharField()
    body = serializers.DictField()
    template = serializers.CharField()
