from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from src.apps.users.enums import UserRoles
from src.apps.users.models import User
from src.apps.users.permissions import IsAuthenticatedOrCreateOnly
from src.apps.users.serializers import (
    PatientUserProfileSerializer,
)


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
