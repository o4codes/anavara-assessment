from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .filters import MedicalRecordFilter
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer


class MedicalRecordViewSet(ModelViewSet):
    queryset = MedicalRecord.objects.all().select_related('doctor', 'patient')
    serializer_class = MedicalRecordSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = MedicalRecordFilter
    ordering_fields = ['created_at', 'updated_at', 'mrid']

