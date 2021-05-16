import datetime
import pytz
from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from server.settings import TIME_ZONE


class CheckTokenExpiration:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        user = request.user

        if request.path != '/login' and user and user.pk and hasattr(user, 'auth_token'):
            utc_now = datetime.datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.timezone(TIME_ZONE))

            token: Token = user.auth_token
            print(request.path, token.created, utc_now)
            if token.created < utc_now - datetime.timedelta(hours=1):
                token.delete()
            else:
                token.created = utc_now
                token.save()

        return self.get_response(request)
