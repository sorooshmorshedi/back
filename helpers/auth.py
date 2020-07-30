from django.contrib.auth.models import Permission
from django.views.generic.base import View
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from helpers.models import BaseModel


def get_codenames(request, view):
    permission_codename = getattr(view, 'permission_codename', None)

    permission_codenames = []
    if permission_codename:
        permission_codenames.append(permission_codename)

        operation = permission_codename.split('.')[0]
        permission_codenames.append(permission_codename.replace(operation, "{}Own".format(operation)))
    else:
        base_codename = getattr(view, 'permission_basename', None)
        if not base_codename:
            raise Exception(
                "permission_basename does not found, declare permission_basename or permission_codename in view"
            )

        method = request.method.upper()

        operations = []
        if method == 'POST':
            operations.append("create")
        if method == 'GET':
            operations.append("get")
            operations.append("getOwn")
        if method == 'PUT':
            operations.append("update")
            operations.append("updateOwn")
        if method == 'DELETE':
            operations.append("delete")
            operations.append("deleteOwn")

        for operation in operations:
            permission_codenames.append("{}.{}".format(operation, base_codename))

    return permission_codenames


class BasicObjectPermission(BasePermission):

    def has_object_permission(self, request: Request, view: View, obj: BaseModel) -> bool:
        user = request.user
        codenames = get_codenames(request, view)

        if user.has_perm(codenames[0]):
            has_perm = True
        else:
            has_perm = request.user.has_object_perm(obj, codenames[1])

        if has_perm and hasattr(obj, 'first_confirmed_at'):
            if obj.has_first_confirmation:
                if obj.has_second_confirmation:
                    return user == obj.second_confirmed_by
                return user == obj.first_confirmed_by or user == obj.second_confirmed_by
            else:
                return True
        else:
            return has_perm


class BasicCRUDPermission(BasicObjectPermission):

    def has_permission(self, request, view):
        return True
        user = request.user

        permission_codenames = get_codenames(request, view)

        for permission_codename in permission_codenames:
            has_perm = user.has_perm(permission_codename)
            if has_perm:
                return True

        permission_codename = permission_codenames[0]
        permission = Permission.objects.filter(codename=permission_codename).first()
        if permission:
            self.message = "شما اجازه این عملیات را ندارید: {}".format(permission.name)
        else:
            self.message = "not found permission: {}".format(permission_codename)

        return False


class TokenAuthSupportQueryString(TokenAuthentication):

    def authenticate(self, request):
        token = request.query_params.get("token", None)

        if token:
            result = self.authenticate_credentials(token)
        else:
            result = super(TokenAuthSupportQueryString, self).authenticate(request)

        return result
