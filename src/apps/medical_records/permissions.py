from rest_framework import permissions

from src.apps.users import enums as user_enums


class MedicalRecordPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == user_enums.UserRoles.DOCTOR

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.doctor.user == request.user

        return True


class PatientMedicalRecordPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == user_enums.UserRoles.DOCTOR:
            return True
        if request.user.role == user_enums.UserRoles.PATIENT:
            if obj.patient.user == request.user:
                return True
        return False
