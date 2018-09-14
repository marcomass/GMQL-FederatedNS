from rest_framework import permissions


class IsAllowedToSeeThis(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # work when your access /item/item_id/
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user