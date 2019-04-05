from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class ModifyRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        data = getattr(request, '_body', request.body)
        request._body = data + '&dummy_param=1'
        # if you call request.body here you will see that new parameter is added

        if request.method == 'POST':
            # user = request.user

            user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

            if user:
                request.body['user'] = user.id
                request.body['financial_year'] = user.active_financial_year.id
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JSONWebTokenAuthentication()
        if jwt_authentication.get_jwt_value(request):
            user, jwt = jwt_authentication.authenticate(request)
        return user

