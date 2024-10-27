from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow access if the form's user matches the requesting user
        return obj.user == request.user
