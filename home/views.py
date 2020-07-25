import datetime

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from home.models import Option
from home.serializers import OptionSerializer


class TimeView(APIView):
    def get(self, request):
        return Response({'time': datetime.datetime.now()})


class OptionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class OptionUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission,)
    permission_basename = 'option'
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
