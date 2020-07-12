from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff or request.user.role == request.user.UserRole.ADMIN)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        #return request.method in permissions.SAFE_METHODS or request.user.is_staff or request.user.role=='admin'
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            request.user.role == request.user.UserRole.ADMIN
        )

class IsStaffOrOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.author == request.user or 
            request.method in permissions.SAFE_METHODS or
            request.user.role == request.user.UserRole.MODERATOR or
            request.user.role == request.user.UserRole.ADMIN
        )
