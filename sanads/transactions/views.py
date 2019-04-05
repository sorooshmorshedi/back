from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from sanads.transactions.serializers import *


@method_decorator(csrf_exempt, name='dispatch')
class TransactionListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = TransactionListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.instance.createSanad(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.inFinancialYear(self.request.user)

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        transaction = self.get_object()
        transaction.updateSanad()
        return res

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        transaction = get_object_or_404(queryset, pk=pk)
        serializer = TransactionListRetrieveSerializer(transaction)
        return Response(serializer.data)


class TransactionItemModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    serializer_class = TransactionItemSerializer

    def get_queryset(self):
        return TransactionItem.objects.inFinancialYear(self.request.user)

    def create(self, request):
        many = True
        if type(request.data) is not list:
            data = request.data
            data['financial_year'] = request.user.active_financial_year.id
            many = False
        else:
            data = []
            for item in request.data:
                item['financial_year'] = request.user.active_financial_year.id
                data.append(item)
        serialized = self.serializer_class(data=data, many=many)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        instance = serialized.instance
        if type(instance) is list:
            if len(instance):
                instance[0].transaction.updateSanad()
        else:
            instance.transaction.updateSanad()
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = TransactionItemListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        transactionItem = get_object_or_404(queryset, pk=pk)
        serializer = TransactionItemListRetrieveSerializer(transactionItem)
        return Response(serializer.data)


class TransactionItemMass(APIView):
    serializer_class = TransactionItemSerializer

    def put(self, request):
        instance = None
        for item in request.data:
            instance = TransactionItem.objects.inFinancialYear(request.user).get(id=item['id'])
            serialized = TransactionItemSerializer(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        res = Response(serialized.data, status=status.HTTP_200_OK)

        if instance:
            instance.transaction.updateSanad()

        return res

    def delete(self, request):
        transaction = None
        for itemId in request.data:
            instance = TransactionItem.objects.inFinancialYear(request.user).get(id=itemId)
            transaction = instance.transaction
            instance.delete()
        if transaction:
            transaction.updateSanad()
        return Response([], status=status.HTTP_200_OK)


@api_view(['get'])
def newCodeForTransaction(request):
    if 'type' not in request.GET:
        return Response(['لطفا نوع را مشخص کنید'], status=status.HTTP_400_BAD_REQUEST)
    else:
        type = request.GET['type']
    try:
        code = Transaction.objects.inFinancialYear(request.user).filter(type=type).latest('code').code + 1
    except:
        code = 1
    return Response(code)


@api_view(['get'])
def getTransactionByCode(request):
    if 'code' not in request.GET:
        return Response(['کد وارد نشده است'], status.HTTP_400_BAD_REQUEST)
    if 'type' not in request.GET:
        return Response(['نوع وارد نشده است'], status.HTTP_400_BAD_REQUEST)

    code = request.GET['code']
    type = request.GET['type']
    queryset = Transaction.objects.inFinancialYear(request.user).all()
    transaction = get_object_or_404(queryset, code=code, type=type)
    serializer = TransactionListRetrieveSerializer(transaction)
    return Response(serializer.data)
