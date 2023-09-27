from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from src.apps.users.enums import UserRoles
from src.apps.users.models import DoctorProfile
from .user import USER_EXCLUDE_FIELDS

PROFILE_EXCLUDE_FIELDS = ["user"]


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        exclude = ["user"]


class DoctorUserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = DoctorProfileSerializer(
        source="doctor",
    )

    class Meta:
        model = get_user_model()
        read_only_fields = ["role"]
        exclude = USER_EXCLUDE_FIELDS

    def create(self, validated_data):
        doctor_profile_data = validated_data.pop("doctor")
        password = validated_data.pop("password")
        validated_data["role"] = UserRoles.DOCTOR
        user = get_user_model()(**validated_data)
        try:
            validate_password(password, user)
        except ValidationError as exception:
            raise serializers.ValidationError({"message": list(exception)})
        user.set_password(password)
        user.save()
        DoctorProfile.objects.create(**doctor_profile_data, user=user)
        return user

    def update(self, instance, validated_data):
        doctor_profile_data = validated_data.pop("doctor", None)
        password = validated_data.pop("password", None)

        if password:
            try:
                validate_password(password, instance)
                instance.set_password(password)
            except ValidationError as exception:
                raise serializers.ValidationError({"message": list(exception)})

        if doctor_profile_data:
            doctor_profile = instance.doctor
            for attr, value in doctor_profile_data.items():
                setattr(doctor_profile, attr, value)
            doctor_profile.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
