from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.medical_records.tests import utils as medical_records_test_utils
from src.apps.users.tests import utils as user_test_utils


class MedicalRecordTests(APITestCase):
    def setUp(self) -> None:
        self.password = "Test#1234"
        self.doctor_one, self.doctor_two = user_test_utils.setup_doctors()
        self.patient_one, self.patient_two = user_test_utils.setup_patients()
        self.medical_record = medical_records_test_utils.setup_medical_record(
            self.patient_one, self.doctor_one
        )

    def test_list_medical_records_success(self):
        url = reverse("medical-records-list")
        user_test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_list_medical_records_failure(self):
        url = reverse("medical-records-list")
        user_test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_medical_record_success(self):
        url = reverse("medical-records-list")
        data = {
            "patient_id": self.patient_one.pk,
            "diagnosis": "Diagnosis of Typhoid",
            "treatment": "Use of some drugs",
        }
        user_test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["mrid"])
        self.assertEqual(
            response.data["patient"]["profile"]["id"], str(data["patient_id"])
        )
        self.assertEqual(
            response.data["doctor"]["profile"]["id"], str(self.doctor_one.pk)
        )
        self.assertEqual(response.data["treatment"], data["treatment"])
        self.assertEqual(response.data["diagnosis"], data["diagnosis"])

    def test_create_medical_record_failure(self):
        url = reverse("medical-records-list")
        data = {
            "patient_id": self.patient_one.pk,
            "diagnosis": "Diagnosis of Typhoid",
            "treatment": "Use of some drugs",
        }
        user_test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_medical_record_success(self):
        url = reverse("medical-records-detail", kwargs={"pk": self.medical_record.pk})
        data = {
            "diagnosis": "Diagnosis of Typhoid",
            "treatment": "Use of some drugs",
        }
        user_test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("doctor").get("profile").get("id"),
            str(self.doctor_one.pk),
        )
        self.assertEqual(response.data.get("treatment"), data["treatment"])
        self.assertEqual(response.data.get("diagnosis"), data["diagnosis"])

    def test_update_medical_record_failure(self):
        url = reverse("medical-records-detail", kwargs={"pk": self.medical_record.pk})
        data = {
            "diagnosis": "Diagnosis of Typhoid",
            "treatment": "Use of some drugs",
        }
        user_test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_medical_record_success(self):
        url = reverse("medical-records-detail", kwargs={"pk": self.medical_record.pk})
        user_test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_medical_record_failure(self):
        url = reverse("medical-records-detail", kwargs={"pk": "1234"})
        user_test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_medical_record_success(self):
        url = reverse("medical-records-detail", kwargs={"pk": self.medical_record.pk})
        user_test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_medical_record_failure(self):
        url = reverse("medical-records-detail", kwargs={"pk": "1234"})
        user_test_utils.authenticate_user(self.client, self.doctor_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
