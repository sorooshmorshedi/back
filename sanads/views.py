from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from sanads.models import *
from sanads.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class RPTypeListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = RPType.objects.all()
    serializer_class = RPTypeSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = RPType.objects.all()
        serializer = RPTypeListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class RPTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    queryset = RPType.objects.all()
    serializer_class = RPTypeSerializer

    def retrieve(self, request, pk=None):
        queryset = RPType.objects.all()
        rptype = get_object_or_404(queryset, pk=pk)
        serializer = RPTypeListRetrieveSerializer(rptype)
        return Response(serializer.data)


