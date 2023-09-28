from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    "medical-records", views.MedicalRecordViewSet, basename="medical-records"
)

urlpatterns = [
    path("", include(router.urls)),
]
