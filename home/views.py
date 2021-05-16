import datetime
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from home.models import Option, DefaultText
from home.serializers import OptionSerializer, DefaultTextSerializer
from server.settings import RECAPTCHA_PRIVATE_KEY


class TimeView(APIView):
    def get(self, request):
        return Response({'time': datetime.datetime.now().timestamp()})


class OptionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class OptionUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'option'
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class DefaultTextView(generics.ListAPIView, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    permission_basename = 'defaultText'
    serializer_class = DefaultTextSerializer

    def get_queryset(self):
        return DefaultText.objects.inFinancialYear()


class ObtainAuthTokenView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_response = request.data.get('recaptchaResponse', None)
        params = urlencode({
            'secret': RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response,
            'remote_ip': request.META.get('REMOTE_ADDR')
        })

        data = urlopen(URIReCaptcha, params.encode('utf-8')).read()
        result = json.loads(data)
        success = result.get('success', None)

        if success:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            raise ValidationError({'non_field_errors': ['ریکپچا غیر قابل قبول می باشد']})
