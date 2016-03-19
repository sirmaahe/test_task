from rest_framework import permissions

from .utils import is_superuser, is_partner, is_credit_organization


class ClientProfilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        as_superuser = is_superuser(request.user) and request.method != 'POST'
        as_partner = (is_partner(request.user) and
                      request.method in permissions.SAFE_METHODS + ('POST',))
        return as_superuser or as_partner

    def has_object_permission(self, request, view, obj):
        return is_superuser(request.user) or obj.partner.id == request.user.id


class CreditApplicationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        as_superuser = is_superuser(request.user) and request.method != 'POST'
        as_credit_organization = (is_credit_organization(request.user) and
                                  request.method in permissions.SAFE_METHODS)
        return as_superuser or as_credit_organization

    def has_object_permission(self, request, view, obj):
        return (is_superuser(request.user) or
                obj.credit_proposal.credit_organization.id == request.user.id)
