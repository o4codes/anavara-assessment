from decouple import config as env_config
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from src.apps.users import models, serializers


class PasswordForgotViewSet(viewsets.ViewSet):
    @extend_schema(
        request=serializers.PasswordForgotSerializer,
        responses={200: serializers.PasswordForgotSerializer},
    )
    def create(self, request):
        email = request.data.get("email")

        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        token = default_token_generator.make_token(user)
        user_id = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate a password reset link with the uid and token
        reset_url = f'{env_config("RESET_PASSWORD_URL")}/{user_id}/{token}/'

        # Send the password reset email to the user
        user.send_reset_email(reset_url)

        return Response({"message": "Password reset email sent"})


class PasswordResetViewSet(viewsets.ViewSet):
    @classmethod
    def reset_password(cls, user_id, token, password):
        # Decode the uid and validate the token
        try:
            user_id = force_str(urlsafe_base64_decode(user_id))
            user = models.User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
            return Response(
                {"message": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response(
                serializers.UserSerializer(user).data, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        request=serializers.PasswordResetSerializer,
        responses={200: serializers.UserSerializer},
    )
    def create(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        response = self.reset_password(user_id, token, password)
        return response
