from rest_framework import serializers


class PasswordForgotSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    message = serializers.CharField(read_only=True)


class PasswordResetSerializer(serializers.Serializer):
    user_id = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
