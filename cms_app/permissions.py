from rest_framework.permissions import BasePermission

class IsAuthorOrAdmin(BasePermission):
    """
    Custom permission to only allow authors of an object to edit it or admins to edit/delete all objects.
    """

    def has_object_permission(self, request, view, obj):
        # Allow full access to admins
        if request.user.user_role == 'Admin':
            return True
        # Allow only the author of the content to edit/delete
        return obj.author == request.user
