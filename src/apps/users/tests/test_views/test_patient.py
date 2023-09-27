from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.users import enums, models
from src.apps.users.tests.utils import authenticate_user


class PatientTests(APITestCase):
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
        self.patient = models.PatientProfile.objects.create(
            user=self.user,
            date_of_birth="2000-01-01",
        )

    def test_list_patients(self):
        url = reverse("patients-list")
        authenticate_user(self.client, self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_create_patient(self):
        url = reverse("patients-list")
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "middle_name": "Test",
            "gender": enums.Gender.MALE.value,
            "email": "test@mail.com",
            "password": "Test#1234",
            "profile": {
                "date_of_birth": "2000-01-01",
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["profile"]["uhid"])

    def test_update_patient(self):
        url = reverse("patients-detail", kwargs={"pk": self.user.pk})
        authenticate_user(self.client, self.user)
        data = {
            "first_name": "Test_Updated",
            "profile": {
                "date_of_birth": "2000-01-02",
            },
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), "Test_Updated")
        self.assertEqual(
            response.data.get("profile").get("date_of_birth"), "2000-01-02"
        )

    def test_delete_patient(self):
        url = reverse("patients-detail", kwargs={"pk": self.user.pk})
        authenticate_user(self.client, self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
