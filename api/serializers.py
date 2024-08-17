
from rest_framework import serializers

class SendEmailSerializer(serializers.Serializer):
    to_email = serializers.EmailField()
