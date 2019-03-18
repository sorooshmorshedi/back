from rest_framework.permissions import BasePermission
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class BasicCRUDPermission(BasePermission):
    def has_permission(self, request, view):
        return True
        model = view.serializer_class.Meta.model
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        method = request.method
        user = request.user

        perm = ''
        if method == 'POST':
            perm = "{}.create_{}".format(app_label, model_name)
        if method == 'GET':
            perm = "{}.retrieve_{}".format(app_label, model_name)
        if method == 'PUT':
            perm = "{}.update_{}".format(app_label, model_name)
        if method == 'DELETE':
            perm = "{}.delete_{}".format(app_label, model_name)

        return user.has_perm(perm)


class TokenAuthSupportQueryString(JSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        token = request.query_params.get('token', None)
        if token:
            return token
        else:
            return super(TokenAuthSupportQueryString, self).get_jwt_value(request)

