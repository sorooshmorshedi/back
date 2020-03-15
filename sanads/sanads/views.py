from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from helpers.views.MassRelatedCUD import MassRelatedCUD
from sanads.sanads.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class SanadListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    serializer_class = SanadSerializer

    def get_queryset(self):
        return Sanad.objects.inFinancialYear()

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = SanadListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        sanad_data = data.get('sanad')
        items_data = data.get('items')

        serializer = SanadSerializer(data=sanad_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            code=newSanadCode(user)
        )

        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'sanad',
            serializer.instance.id,
            SanadItemSerializer,
            SanadItemSerializer,
        ).sync()

        is_confirmed = data.get('_confirmed')
        if not is_confirmed:
            serializer.instance.check_account_balance_confirmations()

        return Response(SanadListRetrieveSerializer(instance=serializer.instance).data, status=status.HTTP_201_CREATED)


class SanadDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    serializer_class = SanadSerializer

    def get_queryset(self):
        return Sanad.objects.inFinancialYear()

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        sanad = get_object_or_404(queryset, pk=pk)
        serializer = SanadListRetrieveSerializer(sanad)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        sanad_data = data.get('sanad')
        items_data = data.get('items')

        serializer = SanadSerializer(instance=self.get_object(), data=sanad_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        MassRelatedCUD(
            user,
            items_data.get('items'),
            items_data.get('ids_to_delete'),
            'sanad',
            serializer.instance.id,
            SanadItemSerializer,
            SanadItemSerializer,
        ).sync()

        is_confirmed = data.get('_confirmed')
        if not is_confirmed:
            serializer.instance.check_account_balance_confirmations()

        return Response(SanadListRetrieveSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)


@api_view(['get'])
def newCodeForSanad(request):
    return Response(newSanadCode(request.user))


@api_view(['get'])
def getSanadByCode(request):
    if 'code' not in request.GET:
        return Response(['کد سند وارد نشده است'], status.HTTP_400_BAD_REQUEST)

    code = request.GET['code']
    queryset = Sanad.objects.inFinancialYear().all()
    sanad = get_object_or_404(queryset, code=code)
    serializer = SanadListRetrieveSerializer(sanad)
    return Response(serializer.data)
