from django.contrib.auth.models import Permission
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import BasePermission


class BasicCRUDPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        permission_codename = getattr(view, 'permission_codename', None)

        if not permission_codename:
            base_codename = getattr(view, 'permission_base_codename', None)
            if not base_codename:
                raise Exception(
                    "permission_base_codename does not found, declare permission_base_codename or permission_codename in view"
                )

            method = request.method

            operation = ''
            if method == 'POST':
                operation = "create"
            if method == 'GET':
                operation = "get"
            if method == 'PUT':
                operation = "update"
            if method == 'DELETE':
                operation = "delete"

            permission_codename = "{}.{}".format(operation, base_codename)

        has_perm = user.has_perm(permission_codename)
        if has_perm:
            return True
        else:
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
