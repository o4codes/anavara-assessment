from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from src.apps.users.enums import UserRoles
from src.apps.users.models import PatientProfile
from .user import USER_EXCLUDE_FIELDS

PROFILE_EXCLUDE_FIELDS = ["user"]


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        exclude = PROFILE_EXCLUDE_FIELDS


class PatientUserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = PatientProfileSerializer(
        source="patient",
    )

    class Meta:
        model = get_user_model()
        read_only_fields = ["role"]
        exclude = USER_EXCLUDE_FIELDS

    def create(self, validated_data):
        patient_profile_data = validated_data.pop("patient")
        password = validated_data.pop("password")
        validated_data["role"] = UserRoles.PATIENT
        user = get_user_model()(**validated_data)
        try:
            validate_password(password, user)
        except ValidationError as exception:
            raise serializers.ValidationError({"message": list(exception)})
        user.set_password(password)
        user.save()
        PatientProfile.objects.create(**patient_profile_data, user=user)
        return user

    def update(self, instance, validated_data):
        patient_profile_data = validated_data.pop("patient", None)
        password = validated_data.pop("password", None)
        if password:
            try:
                validate_password(password, instance)
                instance.set_password(password)
            except ValidationError as exception:
                raise serializers.ValidationError({"message": list(exception)})

        if patient_profile_data:
            patient_profile = instance.patient
            for attr, value in patient_profile_data.items():
                setattr(patient_profile, attr, value)
            patient_profile.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
