from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from src.apps.users import models as user_models

from .filters import MedicalRecordFilter
from .models import MedicalRecord
from .permissions import MedicalRecordPermission, PatientMedicalRecordPermission
from .serializers import MedicalRecordSerializer


class MedicalRecordViewSet(ModelViewSet):
    queryset = MedicalRecord.objects.all().select_related("doctor", "patient")
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, MedicalRecordPermission]
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = MedicalRecordFilter
    ordering_fields = ["created_at", "updated_at", "mrid"]
    search_fields = ["mrid", "treatment", "diagnosis"]


class PatientMedicalRecordViewSet(ReadOnlyModelViewSet):
    serializer_class = MedicalRecordSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    ordering_fields = ["created_at", "updated_at", "mrid"]
    search_fields = ["mrid", "treatment", "diagnosis"]
    permission_classes = [IsAuthenticated, PatientMedicalRecordPermission]

    def get_queryset(self):
        try:
            user_models.PatientProfile.objects.get(pk=self.kwargs["patient_pk"])
        except user_models.PatientProfile.DoesNotExist:
            raise NotFound(detail="Patient not found")
        return MedicalRecord.objects.filter(
            patient__id=self.kwargs["patient_pk"]
        ).select_related("doctor", "patient")
