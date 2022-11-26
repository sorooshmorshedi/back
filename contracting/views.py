from django.db.models import Q
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from contracting.models import Tender, Contract, Statement, Supplement
from contracting.serializers import TenderSerializer, ContractSerializer, StatementSerializer, SupplementSerializer, \
    ContractDetailsSerializer
from helpers.auth import BasicCRUDPermission
from rest_framework import status
from rest_framework.response import Response
from helpers.views.lock_view import ToggleItemLockView
from transactions.models import Transaction


class TenderApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'tender'

    def get(self, request):
        query = Tender.objects.all()
        serializers = TenderSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmedTenderView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'tender'

    def get(self, request, pk):
        tender = Tender.objects.get(pk=pk)
        tender.is_confirmed = True
        tender.save()
        return Response({'confirmed': 'ok'}, status=status.HTTP_200_OK)


class AddTransactionTenderView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'tender'

    def get(self, request, pk1, pk2):
        tender = Tender.objects.get(pk=pk1)
        transaction = Transaction.objects.get(pk=pk2)
        tender.transaction.add(transaction)
        tender.save()
        return Response({'tender transaction': transaction.id}, status=status.HTTP_200_OK)


class TenderDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'tender'

    def get_object(self, pk):
        try:
            return Tender.objects.get(pk=pk)
        except Tender.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = TenderSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = TenderSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleTenderLockView(ToggleItemLockView):
    permission_codename = 'lock.tender'
    serializer_class = TenderSerializer


class DefineTenderView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'define.tender'
    serializer_class = TenderSerializer

    def post(self, request):
        data = request.data
        item = get_object_or_404(
            self.serializer_class.Meta.model,
            pk=data.get('item')
        )

        item.define()

        return Response(self.serializer_class(instance=item).data)


class ContractApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request):
        query = Contract.objects.all()
        serializers = ContractSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddContractReceivedTransactionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request, pk1, pk2):
        contract = Contract.objects.get(pk=pk1)
        transaction = Transaction.objects.get(pk=pk2)
        contract.received_transaction.add(transaction)
        contract.save()
        return Response({'contract received transaction': transaction.id}, status=status.HTTP_200_OK)


class AddContractPaymentTransactionView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request, pk1, pk2):
        contract = Contract.objects.get(pk=pk1)
        transaction = Transaction.objects.get(pk=pk2)
        contract.guarantee_document_transaction.add(transaction)
        contract.save()
        return Response({'contract guarantee document transaction': transaction.id}, status=status.HTTP_200_OK)


class ContractPreviousValue(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request, pk):
        contract = Contract.objects.get(id=pk)
        previous_value = 0
        statements = Statement.objects.filter(contract=contract)
        for statement in statements:
            previous_value += statement.value
        return Response(previous_value, status=status.HTTP_200_OK)


class ContractChange(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request, pk):
        contract = Contract.objects.get(id=pk)
        change = contract.amount
        change1 = (change / 100) * contract.max_change_amount
        m = change - change1
        n = change + change1
        return Response({'min': m, 'max': n}, status=status.HTTP_200_OK)


class ContractDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ContractSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ContractSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractAllDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        contract = self.get_object(pk)
        received_transaction = contract.received_transaction.all()
        guarantee_transaction = contract.guarantee_document_transaction.all()
        serializers = ContractDetailsSerializer(contract)
        return Response({'contract': serializers.data, 'received_transaction': received_transaction,
                         'guarantee_transaction': guarantee_transaction}, status=status.HTTP_200_OK)


class ToggleContractLockView(ToggleItemLockView):
    permission_codename = 'lock.contract'
    serializer_class = ContractSerializer


class DefineContractView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'define.contract'
    serializer_class = ContractSerializer

    def post(self, request):
        data = request.data
        item = get_object_or_404(
            self.serializer_class.Meta.model,
            pk=data.get('item')
        )

        item.define()

        return Response(self.serializer_class(instance=item).data)


class StatementApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'statement'

    def get(self, request):
        query = Statement.objects.all()
        serializers = StatementSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StatementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatementDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'statement'

    def get_object(self, pk):
        try:
            return Statement.objects.get(pk=pk)
        except Statement.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = StatementSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = StatementSerializer(query, data=request.data)
        if serializer.is_valid():
            next_statements = Statement.objects.filter(Q(contract_id=query.contract.id)
                                                       & Q(id__gt=query.id)).order_by('id')
            print(next_statements)
            serializer.save()
            print(next_statements)
            for statement in next_statements:
                statement.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        next_statements = Statement.objects.filter(Q(contract_id=query.contract.id)
                                                   & Q(id__gt=query.id)).order_by('id')
        query.delete()
        for statement in next_statements:
            statement.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleStatementLockView(ToggleItemLockView):
    permission_codename = 'lock.statement'
    serializer_class = StatementSerializer


class DefineStatementView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'define.statement'
    serializer_class = StatementSerializer

    def post(self, request):
        data = request.data
        item = get_object_or_404(
            self.serializer_class.Meta.model,
            pk=data.get('item')
        )

        item.define()

        return Response(self.serializer_class(instance=item).data)


class SupplementApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'supplement'

    def get(self, request):
        query = Supplement.objects.all()
        serializers = SupplementSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SupplementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplementDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'supplement'

    def get_object(self, pk):
        try:
            return Supplement.objects.get(pk=pk)
        except Supplement.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = SupplementSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = SupplementSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleSupplementLockView(ToggleItemLockView):
    permission_codename = 'lock.supplement'
    serializer_class = SupplementSerializer


class DefineSupplementView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'define.supplement'
    serializer_class = SupplementSerializer

    def post(self, request):
        data = request.data
        item = get_object_or_404(
            self.serializer_class.Meta.model,
            pk=data.get('item')
        )

        item.define()

        return Response(self.serializer_class(instance=item).data)

