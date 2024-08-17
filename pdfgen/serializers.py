
from rest_framework import serializers

class JsonToPdfSerializer(serializers.Serializer):
    data = serializers.JSONField()
