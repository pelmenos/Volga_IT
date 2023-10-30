from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRenter(BasePermission):
    def has_permission(self, request, view):
        return request.user.rents.filter(id=view.kwargs['pk']).exists()

    def has_object_permission(self, request, view, obj):
        return obj.renter == request.user


class IsTransportOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.transports.filter(id=view.kwargs['pk']).exists()

    def has_object_permission(self, request, view, obj):
        return obj.transport.owner == request.user
