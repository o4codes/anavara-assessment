from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .enums import UserRoles
from .models import User
from .permissions import IsAuthenticatedOrCreateOnly
from .serializers import PatientUserProfileSerializer, DoctorUserProfileSerializer


class PatientUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=UserRoles.PATIENT)
    serializer_class = PatientUserProfileSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["created_at", "updated_at"]
    search_fields = ["first_name", "last_name", "email"]


class DoctorUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=UserRoles.DOCTOR)
    serializer_class = DoctorUserProfileSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["created_at", "updated_at"]
    search_fields = ["first_name", "last_name", "email"]