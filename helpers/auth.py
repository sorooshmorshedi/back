from django.contrib.auth.models import Permission
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import BasePermission


class BasicCRUDPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        permission_codename = getattr(view, 'permission_codename', None)

        permission_codenames = []
        if permission_codename:
            permission_codenames.append(permission_codename)

            operation = permission_codename.split('.')[0]
            permission_codenames.append(permission_codename.replace(operation, "{}Own".format(operation)))
        else:
            base_codename = getattr(view, 'permission_base_codename', None)
            if not base_codename:
                raise Exception(
                    "permission_base_codename does not found, declare permission_base_codename or permission_codename in view"
                )

            method = request.method

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
