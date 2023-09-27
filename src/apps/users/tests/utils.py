from rest_framework_simplejwt.tokens import RefreshToken


def authenticate_user(client, user):
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token))
