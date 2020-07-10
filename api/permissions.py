from rest_framework import permissions


class GenrePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(
            request.auth and (
                request.user.is_superuser or request.user.role == 'admin'
            )
        )