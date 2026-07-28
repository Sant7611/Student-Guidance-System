from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Allows any authenticated user through at the view level; the individual
    dashboard views already check request.user.role themselves.
    Object-level checks still restrict to the actual owner.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj == request.user or bool(request.user and request.user.is_staff)


class AdminOnlyPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
