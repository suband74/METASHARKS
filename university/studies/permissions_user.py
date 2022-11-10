from rest_framework import permissions

from .models import UserRole


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and UserRole.ADMIN in request.user.roles
            and request.user.is_staff
        )


class IsAdminOrCurator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.user
                and UserRole.ADMIN in request.user.roles
                and request.user.is_staff
            )
            or (
                request.user.is_authenticated and UserRole.CURATOR in request.user.roles
            )
        )


class IsCurator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and UserRole.CURATOR in request.user.roles
