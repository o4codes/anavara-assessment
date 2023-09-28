from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.apps.users import enums as user_enums
from src.apps.users import models as user_models
from src.apps.users import serializers as user_serializers

from .models import MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=user_models.PatientProfile.objects.all(),
        source="patient",
        write_only=True,
    )
    patient = user_serializers.PatientUserProfileSerializer(
        read_only=True, source="patient.user"
    )
    doctor = user_serializers.DoctorUserProfileSerializer(
        read_only=True, source="doctor.user"
    )

    class Meta:
        model = MedicalRecord
        fields = "__all__"
        read_only_fields = ["mrid", "created_at", "updated_at", "patient", "doctor"]

    def validate(self, attrs):
        user = self.context["request"].user
        attrs["doctor"] = user.doctor
        return attrs
