from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.medical_records.tests import utils as medical_records_test_utils
from src.apps.users.tests import utils as user_test_utils


class PatientMedicalRecordTests(APITestCase):
    def setUp(self) -> None:
        self.password = "Test#1234"
        self.doctor_one, self.doctor_two = user_test_utils.setup_doctors()
        self.patient_one, self.patient_two = user_test_utils.setup_patients()
        self.medical_record = medical_records_test_utils.setup_medical_record(
            self.patient_one, self.doctor_one
        )

    def test_list_patient_medical_records(self):
        url = reverse(
            "patient_medical_records-list", kwargs={"patient_pk": self.patient_one.pk}
        )
        user_test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_list_patient_medical_records_failure(self):
        url = reverse(
            "patient_medical_records-list", kwargs={"patient_pk": self.patient_two.pk}
        )
        user_test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_patient_medical_record(self):
        url = reverse(
            "patient_medical_records-detail",
            kwargs={"patient_pk": self.patient_one.pk, "pk": self.medical_record.pk},
        )
        user_test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("mrid"), self.medical_record.mrid)

    def test_get_patient_medical_record_failure(self):
        url = reverse(
            "patient_medical_records-detail",
            kwargs={"patient_pk": self.patient_two.pk, "pk": self.medical_record.pk},
        )
        user_test_utils.authenticate_user(self.client, self.patient_one.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
