from rest_framework import serializers


class WebhookSerializer(serializers.Serializer):
    webhook_url = serializers.URLField(required=True)


class LoginSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, max_length=6)
    