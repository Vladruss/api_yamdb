from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and  (request.user.is_staff or request.user.role == 'admin'))

class GenrePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(request.user.is_authenticated and  (request.user.is_staff or request.user.role == 'admin'))
    
class AuthorRightPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method=='POST':
            return request.user.is_authenticated
        return obj.author == request.user or request.method in permissions.SAFE_METHODS

class CommentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        '''if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS'''
        return bool((obj.author == request.user and  request.auth )or request.method in permissions.SAFE_METHODS or (request.user.role == 'admin' and request.auth) or (request.user.role == 'moderator' and request.auth) )
