from django.template.backends import django
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

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
        if type(request.data) is not list:
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


class SanadItemMass(APIView):
    serializer_class = SanadItemSerializer

    def put(self, request):
        for item in request.data:
            instance = SanadItem.objects.get(id=item['id'])
            serialized = SanadItemSerializer(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request):
        for itemId in request.data:
            instance = SanadItem.objects.get(id=itemId)
            instance.delete()
        return Response([], status=status.HTTP_200_OK)


class SanadItemDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    queryset = SanadItem.objects.all()
    serializer_class = SanadItemSerializer

    def retrieve(self, request, pk=None):
        queryset = SanadItem.objects.all()
        sanadItem = get_object_or_404(queryset, pk=pk)
        serializer = SanadItemListRetrieveSerializer(sanadItem)
        return Response(serializer.data)


@api_view(['get'])
def newCodeForSanad(request):
    return Response(newSanadCode())


@api_view(['get'])
def getSanadByCode(request):
    if 'code' not in request.GET:
        return Response(['کد سند وارد نشده است'], status.HTTP_400_BAD_REQUEST)

    code = request.GET['code']
    queryset = Sanad.objects.all()
    sanad = get_object_or_404(queryset, code=code)
    serializer = SanadListRetrieveSerializer(sanad)
    return Response(serializer.data)

