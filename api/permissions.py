from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff or request.user.role=='admin')


class GenrePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(request.user.is_staff or request.user.role=='admin')
    

class CommentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.author==request.user or request.method in permissions.SAFE_METHODS or request.user.role=='admin' or request.user.role=='moderator')
