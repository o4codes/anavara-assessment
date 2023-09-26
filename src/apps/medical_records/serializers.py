from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from src.apps.users import enums as user_enums
from .models import MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_id = serializers.HiddenField(
        source="doctor",
        write_only=True,
        default=serializers.CurrentUserDefault()
    )
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(role=user_enums.UserRoles.PATIENT),
        source="patient",
        write_only=True
    )

    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ['mrid', 'created_at', 'updated_at', "patient", "doctor"]
        depth = 2

    def validate_doctor(self, value: get_user_model()):
        if value.role != user_enums.UserRoles.DOCTOR:
            raise serializers.ValidationError(
                {
                    "message": "Only doctors can create medical records"
                }
            )
        return value

    def update(self, instance, validated_data):
        if instance.doctor != validated_data.get("doctor"):
            raise PermissionDenied(
                detail={
                    "message": "Inadequate Permission to edit this medical record"
                }
            )
        return super().update(instance, validated_data)

