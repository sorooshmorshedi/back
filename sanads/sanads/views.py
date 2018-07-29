from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from sanads.models import *
from sanads.sanads.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class SanadListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = Sanad.objects.all()
    serializer_class = SanadSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = Sanad.objects.all()
        serializer = SanadListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class SanadDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    queryset = Sanad.objects.all()
    serializer_class = SanadSerializer

    def retrieve(self, request, pk=None):
        queryset = Sanad.objects.all()
        sanad = get_object_or_404(queryset, pk=pk)
        serializer = SanadListRetrieveSerializer(sanad)
        return Response(serializer.data)


class SanadItemListCreate(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = SanadItem.objects.all()
    serializer_class = SanadItemSerializer

    def create(self, request):
        if type(request.data) is dict:
            return super().create(request)
        serialized = self.serializer_class(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *ergs, **kwargs):
        queryset = SanadItem.objects.all()
        serializer = SanadItemListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class SanadItemDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    queryset = SanadItem.objects.all()
    serializer_class = SanadItemSerializer

    def retrieve(self, request, pk=None):
        queryset = SanadItem.objects.all()
        sanadItem = get_object_or_404(queryset, pk=pk)
        serializer = SanadItemListRetrieveSerializer(sanadItem)
        return Response(serializer.data)
