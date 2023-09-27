from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.users import enums
from src.apps.users.tests import utils as test_utils


class PatientTests(APITestCase):
    def setUp(self) -> None:
        self.password = "Test#1234"
        self.patient_one, self.patient_two = test_utils.setup_patients()

    def test_list_patients(self):
        url = reverse("patients-list")
        test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_create_patient(self):
        url = reverse("patients-list")
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "middle_name": "Test",
            "gender": enums.Gender.MALE.value,
            "email": "toast@mail.com",
            "password": "Taost#1234",
            "profile": {
                "date_of_birth": "2000-01-01",
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["profile"]["uhid"])

    def test_update_patient_sucess(self):
        url = reverse("patients-detail", kwargs={"pk": self.patient_one.user.pk})
        test_utils.authenticate_user(self.client, self.patient_one.user)
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

    def test_update_patient_failure(self):
        url = reverse("patients-detail", kwargs={"pk": self.patient_two.user.pk})
        test_utils.authenticate_user(self.client, self.patient_one.user)
        data = {
            "first_name": "Test_Updated",
            "profile": {
                "date_of_birth": "2000-01-02",
            },
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_patient_success(self):
        url = reverse("patients-detail", kwargs={"pk": self.patient_one.user.pk})
        test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_patient_failure(self):
        url = reverse("patients-detail", kwargs={"pk": self.patient_two.user.pk})
        test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_patient_success(self):
        url = reverse("patients-detail", kwargs={"pk": self.patient_one.user.pk})
        test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_patient_failure(self):
        url = reverse("patients-detail", kwargs={"pk": "1234"})
        test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
