from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    """
    Custom permission to allow only students to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to allow only teachers to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher
