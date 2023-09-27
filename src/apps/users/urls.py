from django.urls import include, path
from rest_framework_nested import routers

from src.apps.medical_records import views as medical_records_views

from . import views

router = routers.DefaultRouter()
router.register("patients", views.PatientUserViewSet, basename="patients")
router.register("doctors", views.DoctorUserViewSet)

patient_router = routers.NestedDefaultRouter(router, "patients", lookup="patient")
patient_router.register(
    "medical_records",
    medical_records_views.PatientMedicalRecordViewSet,
    basename="patient_medical_records",
)

urlpatterns = [
    path("users/", include(router.urls)),
    path("users/", include(patient_router.urls)),
]
