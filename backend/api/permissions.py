from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.exceptions import MethodNotAllowed  # type: ignore


class AuthorOnly(IsAuthenticated):
    def has_object_permission(self, request, view, recipe):
        return (recipe.author == request.user
                or request.user.is_superuser_or_admin)


class ForbiddenPermission(IsAuthenticated):
    def has_permission(self, request, view):
        raise MethodNotAllowed(request.method)
