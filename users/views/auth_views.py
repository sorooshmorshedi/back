import json
from urllib.parse import urlencode
from urllib.request import urlopen

import pyotp
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from server.settings import RECAPTCHA_PRIVATE_KEY


class SecretKeyView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def verify(secret_key, code):
        totp = pyotp.TOTP(secret_key)

        is_verified = totp.verify(code)
        if is_verified:
            return True
        else:
            raise ValidationError("کد قابل قبول نمی باشد")

    def get(self, request):
        secret_key = pyotp.random_base32()
        return Response({
            'secret_key': secret_key,
            'qr_code': pyotp.totp.TOTP(secret_key).provisioning_uri(name=request.user.username, issuer_name="سبحان")
        })

    def put(self, request):
        data = self.request.data
        secret_key = data.get('secret_key', '')
        code = data.get('code', '')

        user = request.user

        if user.secret_key is not None:
            return Response(["ورود دو عاملی برای شما فعال شده است"], status=status.HTTP_400_BAD_REQUEST)

        if self.verify(secret_key, code):
            user.secret_key = request.data.get('secret_key')
            user.save()

        return Response([])

    def delete(self, request):
        user = request.user
        code = request.data.get('code', '')
        if self.verify(user.secret_key, code):
            user.secret_key = None
            user.save()

        return Response([])


class ObtainAuthTokenView(ObtainAuthToken):

    def verify_recaptcha(self):
        URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_response = self.request.data.get('recaptchaResponse', None)
        params = urlencode({
            'secret': RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response,
            'remote_ip': self.request.META.get('REMOTE_ADDR')
        })

        recaptcha_data = urlopen(URIReCaptcha, params.encode('utf-8')).read()
        result = json.loads(recaptcha_data)
        success = result.get('success', None)

        if not success:
            raise ValidationError({'non_field_errors': ['ریکپچا غیر قابل قبول می باشد']})
        return True

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user.secret_key:
            code = request.data.get('code', None)
            if code:
                SecretKeyView.verify(user.secret_key, code)
            else:
                return Response({'need_two_factor_authentication': True})

        self.verify_recaptcha()

        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'need_two_factor_authentication': False,
            'token': token.key
        })
