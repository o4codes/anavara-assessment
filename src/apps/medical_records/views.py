from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

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
        User = get_user_model()
        try:
            user = User.objects.get(pk=self.kwargs["patient_pk"])
        except User.DoesNotExist:
            raise NotFound(detail="Patient not found")
        return MedicalRecord.objects.filter(
            patient__user__id=self.kwargs["patient_pk"]
        ).select_related("doctor", "patient")
