from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'SUPERUSER'


class IsAdministrator(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type in ['SUPERUSER', 'ADMINISTRATOR']


class IsUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type in ['SUPERUSER', 'ADMINISTRATOR', 'USER']


class IsAdministratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.type in ['SUPERUSER', 'ADMINISTRATOR']


class IsSuperUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.type == 'SUPERUSER'