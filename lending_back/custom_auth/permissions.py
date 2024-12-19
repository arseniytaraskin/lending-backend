from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Allows access only to superuser.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsAdmin(BasePermission):
    """
    Allows access only to admin.
    """
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)


class IsStaff(BasePermission):
    """
    Allows access only to staff.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)