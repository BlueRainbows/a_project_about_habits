from rest_framework import permissions


class PermissionUser(permissions.BasePermission):
    """
    Проверка доступа к ресурсу у пользователя,
    если пользователь является создателем объекта,
    то возвращает True, иначе False.
    """
    message = 'User have insufficient rights to perform this action.'

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
