from django.contrib.auth.models import Permission
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import BasePermission


class BasicCRUDPermission(BasePermission):

    def has_permission(self, request, view):
        base_name = getattr(view, 'permission_base_codename', None)
        if not base_name:
            raise Exception("permission base codename does not found")

        method = request.method
        user = request.user

        operation = ''
        if method == 'POST':
            operation = "create"
        if method == 'GET':
            operation = "get"
        if method == 'PUT':
            operation = "update"
        if method == 'DELETE':
            operation = "delete"

        permission_codename = "{}.{}".format(operation, base_name)

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
