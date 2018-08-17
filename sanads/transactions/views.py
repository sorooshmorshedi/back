from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from sanads.transactions.serializers import *

@method_decorator(csrf_exempt, name='dispatch')
class TransactionListCreate(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = Transaction.objects.all()
        serializer = TransactionListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated, RPTypeDetail,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def retrieve(self, request, pk=None):
        queryset = Transaction.objects.all()
        transaction = get_object_or_404(queryset, pk=pk)
        serializer = TransactionListRetrieveSerializer(transaction)
        return Response(serializer.data)


class TransactionItemModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = TransactionItem.objects.all()
    serializer_class = TransactionItemSerializer

    def create(self, request):
        if type(request.data) is not list:
            return super().create(request)
        serialized = self.serializer_class(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *ergs, **kwargs):
        queryset = TransactionItem.objects.all()
        serializer = TransactionItemListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TransactionItem.objects.all()
        transactionItem = get_object_or_404(queryset, pk=pk)
        serializer = TransactionItemListRetrieveSerializer(transactionItem)
        return Response(serializer.data)


class TransactionItemMass(APIView):
    serializer_class = TransactionItemSerializer

    def put(self, request):
        for item in request.data:
            instance = TransaItem.objects.get(id=item['id'])
            serialized = TransactionItemSerializer(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request):
        for itemId in request.data:
            instance = TransactionItem.objects.get(id=itemId)
            instance.delete()
        return Response([], status=status.HTTP_200_OK)
