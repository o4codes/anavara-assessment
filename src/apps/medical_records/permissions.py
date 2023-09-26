from rest_framework import permissions

from src.apps.users import enums as user_enums


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == user_enums.UserRoles.DOCTOR

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.doctor.user == request.user

        return True
