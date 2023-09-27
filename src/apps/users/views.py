from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, filters, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .enums import UserRoles
from .models import User
from .permissions import IsAuthenticatedOrCreateOnly
from .serializers import (
    PatientUserProfileSerializer,
    DoctorUserProfileSerializer,
    UserTokenObtainResponseSerializer,
    UserTokenObtainRequestSerializer,
    UserSerializer,
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


@extend_schema_view(
    post=extend_schema(
        request=UserTokenObtainRequestSerializer,
        responses={200: UserTokenObtainResponseSerializer},
    )
)
class UserTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user_data = UserSerializer(serializer.user).data
            validated_data = serializer.validated_data
            validated_data["user"] = user_data

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(validated_data, status=status.HTTP_200_OK)
