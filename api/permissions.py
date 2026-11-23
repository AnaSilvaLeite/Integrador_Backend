
from rest_framework.permissions import BasePermission, SAFE_METHODS
# BasePermission: É a classe base do DRF usada para criar regras de acesso personalizadas.
# SAFE_METHODS: Métodos HTTP considerados "seguros" (apenas leitura, que não alteram dados no servidor): 'GET', 'HEAD' e 'OPTIONS'.


class IsAdministratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_superuser
            or request.user.type in [
                'SUPERUSER',
                'ADMINISTRATOR'
            ]
        )


class IsSuperUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_superuser
