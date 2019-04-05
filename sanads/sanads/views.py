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
from sanads.sanads.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class SanadListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    serializer_class = SanadSerializer

    def get_queryset(self):
        return Sanad.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = SanadListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        request.data['code'] = newSanadCode(request.user)
        return super().create(request, *args, **kwargs)


class SanadDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    serializer_class = SanadSerializer

    def get_queryset(self):
        return Sanad.objects.inFinancialYear(self.request.user)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        sanad = get_object_or_404(queryset, pk=pk)
        serializer = SanadListRetrieveSerializer(sanad)
        return Response(serializer.data)


class SanadItemListCreate(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    serializer_class = SanadItemSerializer

    def get_queryset(self):
        return Sanad.objects.inFinancialYear(self.request.user)

    def create(self, request):
        if type(request.data) is not list:
            request.data['financial_year'] = request.user.active_financial_year.id
            return super().create(request)
        data = []
        for item in request.data:
            item['financial_year'] = request.user.active_financial_year.id
            data.append(item)
        serialized = self.serializer_class(data=data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = SanadItemListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class SanadItemMass(APIView):
    serializer_class = SanadItemSerializer

    def put(self, request):
        for item in request.data:
            instance = SanadItem.objects.inFinancialYear(request.user).get(id=item['id'])
            serialized = SanadItemSerializer(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request):
        for itemId in request.data:
            instance = SanadItem.objects.inFinancialYear(request.user).get(id=itemId)
            instance.delete()
        return Response([], status=status.HTTP_200_OK)


class SanadItemDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    serializer_class = SanadItemSerializer

    def get_queryset(self):
        return Sanad.objects.inFinancialYear(self.request.user)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        sanadItem = get_object_or_404(queryset, pk=pk)
        serializer = SanadItemListRetrieveSerializer(sanadItem)
        return Response(serializer.data)


@api_view(['get'])
def newCodeForSanad(request):
    return Response(newSanadCode(request.user))


@api_view(['get'])
def getSanadByCode(request):
    if 'code' not in request.GET:
        return Response(['کد سند وارد نشده است'], status.HTTP_400_BAD_REQUEST)

    code = request.GET['code']
    queryset = Sanad.objects.inFinancialYear(request.user).all()
    sanad = get_object_or_404(queryset, code=code)
    serializer = SanadListRetrieveSerializer(sanad)
    return Response(serializer.data)

