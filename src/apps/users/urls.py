from django.urls import include, path
from rest_framework_nested import routers

from src.apps.medical_records import views as medical_records_views

from . import views

router = routers.DefaultRouter()
router.register("patients", views.PatientUserViewSet, basename="patients")
router.register("doctors", views.DoctorUserViewSet, basename="doctors")

patient_router = routers.NestedDefaultRouter(router, "patients", lookup="patient")
patient_router.register(
    "medical_records",
    medical_records_views.PatientMedicalRecordViewSet,
    basename="patient_medical_records",
)

auth_router = routers.DefaultRouter()
auth_router.register(
    "password/forgot", views.PasswordForgotViewSet, basename="forgot-password"
)
auth_router.register(
    "password/reset", views.PasswordResetViewSet, basename="reset-password"
)

urlpatterns = [
    path("users/", include(router.urls)),
    path("users/", include(patient_router.urls)),
    path("auth/", include(auth_router.urls)),
]
