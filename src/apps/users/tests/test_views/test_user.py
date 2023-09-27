from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.users import models, enums


class UserAuthTests(APITestCase):
    def setUp(self) -> None:
        self.password = "Test#1234"
        self.user = models.User.objects.create_user(
            email="test",
            password=self.password,
            first_name="Test",
            last_name="Test",
            middle_name="Test",
            gender=enums.Gender.MALE,
            role=enums.UserRoles.PATIENT,
        )

    def test_user_token_obtain_success(self):
        url = reverse("token_obtain_pair")
        data = {"email": self.user.email, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(response.data.keys()), ["refresh", "access", "user"])

    def test_user_token_obtain_error(self):
        url = reverse("token_obtain_pair")
        data = {"email": "test", "password": "Test1234"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_token_refresh_success(self):
        url = reverse("token_obtain_pair")
        data = {"email": self.user.email, "password": self.password}
        response = self.client.post(url, data, format="json")
        refresh_token = response.data["refresh"]
        url = reverse("token_refresh")
        data = {"refresh": refresh_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(response.data.keys()), ["access"])

    def test_user_token_refresh_failure(self):
        url = reverse("token_refresh")
        data = {"refresh": "test"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
