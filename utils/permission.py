# permissions.py
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to check if the user is an admin.
    """

    def has_permission(self, request, view):
        # Implement your logic here to determine admin status
        try:
            if request.user.isAdmin:
                return True
            return False
        except AttributeError:
            return False


class IsHeadUser(permissions.BasePermission):
    """
    Custom permission to check if the user is a head.
    """

    def has_permission(self, request, view):
        try:
            if request.user.headId is None or request.user.headId:
                return True
            return False
        except AttributeError:
            return False


class IsAccessToMatrimonialAndResidents(permissions.BasePermission):
    """
    Custom permission to check if the user is approved by admin or head.
    """

    def has_permission(self, request, view):
        try:
            if not request.user.isActive:
                raise PermissionDenied('Please wait for admin approval.')
            return True
        except AttributeError:
            return False

