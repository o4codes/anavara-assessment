from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .enums import UserRoles
from .models import PatientProfile, DoctorProfile

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
        validated_data['role'] = UserRoles.PATIENT
        user = get_user_model()(**validated_data)
        validate_password(password, user)
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
                raise serializers.ValidationError(str(exception))

        if patient_profile_data:
            patient_profile = instance.patient
            for attr, value in patient_profile_data.items():
                setattr(patient_profile, attr, value)
            patient_profile.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
        validated_data['role'] = UserRoles.DOCTOR
        user = get_user_model()(**validated_data)
        validate_password(password, user)
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
                raise serializers.ValidationError(str(exception))

        if doctor_profile_data:
            doctor_profile = instance.doctor
            for attr, value in doctor_profile_data.items():
                setattr(doctor_profile, attr, value)
            doctor_profile.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
