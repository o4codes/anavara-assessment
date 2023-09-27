from django.contrib.auth import get_user_model
from rest_framework import serializers

USER_EXCLUDE_FIELDS = [
    "groups",
    "user_permissions",
    "is_superuser",
    "is_staff",
    "is_active",
    "created_at",
    "updated_at",
    "last_login",
]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = USER_EXCLUDE_FIELDS + ["password"]


class UserTokenObtainRequestSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserTokenObtainResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer(read_only=True)
