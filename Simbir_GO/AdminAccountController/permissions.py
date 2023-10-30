from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user.isAdmin):
            raise PermissionDenied({'message': 'Forbidden for you'})

        return bool(request.user.isAdmin)
