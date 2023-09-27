from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.users import enums
from src.apps.users.tests import utils as test_utils


class DocotorTests(APITestCase):
    def setUp(self) -> None:
        self.password = "Test#1234"
        self.doctor_one, self.doctor_two = test_utils.setup_doctors()

    def test_list_doctors(self):
        url = reverse("doctors-list")
        test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_create_doctor(self):
        url = reverse("doctors-list")
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "middle_name": "Test",
            "gender": enums.Gender.MALE.value,
            "email": "toast@mail.com",
            "password": "Taost#1234",
            "profile": {
                "specialization": "Cardiologist",
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["profile"]["umid"])

    def test_update_doctor_success(self):
        url = reverse("doctors-detail", kwargs={"pk": self.doctor_one.user.pk})
        test_utils.authenticate_user(self.client, self.doctor_one.user)
        data = {
            "first_name": "Test_Updated",
            "profile": {
                "specialization": "Surgical Pathologist",
            },
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), "Test_Updated")
        self.assertEqual(
            response.data.get("profile").get("specialization"), "Surgical Pathologist"
        )

    def test_update_doctor_failure(self):
        url = reverse("doctors-detail", kwargs={"pk": self.doctor_two.user.pk})
        test_utils.authenticate_user(self.client, self.doctor_one.user)
        data = {
            "first_name": "Test_Updated",
            "profile": {
                "specialization": "Surgical Pathologist",
            },
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_doctor_success(self):
        url = reverse("doctors-detail", kwargs={"pk": self.doctor_one.user.pk})
        test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_doctor_failure(self):
        url = reverse("doctors-detail", kwargs={"pk": self.doctor_two.user.pk})
        test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_doctor_success(self):
        url = reverse("doctors-detail", kwargs={"pk": self.doctor_one.user.pk})
        test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_doctor_failure(self):
        url = reverse("doctors-detail", kwargs={"pk": "1234"})
        test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
