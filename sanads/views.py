from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics

from sanad.models import *
from sanad.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class RPTypeListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = RPType.objects.all()
    serializer_class = RPTypeSerializer


class RPTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    queryset = RPType.objects.all()
    serializer_class = RPTypeSerializer
