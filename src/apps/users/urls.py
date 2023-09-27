from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("patients", views.PatientUserViewSet)
router.register("doctors", views.DoctorUserViewSet)

urlpatterns = [
    path("users/", include(router.urls)),
]
