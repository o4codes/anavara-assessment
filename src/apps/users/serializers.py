from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import PatientProfile, DoctorProfile


USER_EXCLUDE_FIELDS = [
    "groups",
    "user_permissions",
    "is_superuser",
    "is_staff",
    "is_active",
    "password",
    "created_at",
    "updated_at",
    "last_login",
]
PROFILE_EXCLUDE_FIELDS = ["user"]


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        exclude = PROFILE_EXCLUDE_FIELDS


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        exclude = ["user"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = PROFILE_EXCLUDE_FIELDS


class UserPatientProfileSerializer(serializers.ModelSerializer):
    profile = PatientProfileSerializer(
        read_only=True,
        source="user.patient",
    )

    class Meta:
        model = get_user_model()
        exclude = USER_EXCLUDE_FIELDS


class UserDoctorProfileSerializer(serializers.ModelSerializer):
    profile = DoctorProfileSerializer(
        read_only=True,
        source="user.doctor",
    )

    class Meta:
        model = get_user_model()
        exclude = USER_EXCLUDE_FIELDS
