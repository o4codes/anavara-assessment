from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.apps.users import enums as user_enums
from src.apps.users import serializers as user_serializers
from .models import MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_id = serializers.HiddenField(
        source="doctor", write_only=True, default=serializers.CurrentUserDefault()
    )
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(role=user_enums.UserRoles.PATIENT),
        source="patient",
        write_only=True,
    )
    patient = user_serializers.UserPatientProfileSerializer(
        read_only=True, source="patient.user"
    )
    doctor = user_serializers.UserDoctorProfileSerializer(
        read_only=True, source="doctor.user"
    )

    class Meta:
        model = MedicalRecord
        fields = "__all__"
        read_only_fields = ["mrid", "created_at", "updated_at", "patient", "doctor"]

    def validate_doctor(self, value: get_user_model()):
        if value.role != user_enums.UserRoles.DOCTOR:
            raise serializers.ValidationError(
                {"message": "Only doctors can create medical records"}
            )
        return value
