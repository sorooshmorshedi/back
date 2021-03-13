import datetime
import pytz
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.authtoken.models import Token
from rest_framework.request import Request


class CheckTokenExpiration:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        user = request.user

        if request.path != '/login' and user and user.pk:
            utc_now = datetime.datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)

            token: Token = user.auth_token
            if token.created < utc_now - datetime.timedelta(hours=1):
                token.delete()
            else:
                token.created = utc_now
                token.save()

        return self.get_response(request)
