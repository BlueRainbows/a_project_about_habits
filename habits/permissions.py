from rest_framework import permissions


class PermissionUser(permissions.BasePermission):
    message = 'User have insufficient rights to perform this action.'

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
