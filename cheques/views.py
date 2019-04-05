from django.db import connection
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.defaultAccounts.models import getDA
from cheques.serializers import *


class ChequebookModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChequebookSerializer

    def get_queryset(self):
        return Chequebook.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = ChequebookListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        chequebook = get_object_or_404(queryset, pk=pk)
        serializer = ChequebookListRetrieveSerializer(chequebook)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class ChequeModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChequeSerializer
    queryset = Cheque.objects.all()

    def get_queryset(self):
        return Cheque.objects.inFinancialYear(self.request.user)

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset().filter(received_or_paid=Cheque.RECEIVED)
        serializer = ChequeListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        cheque = get_object_or_404(queryset, pk=pk)
        serializer = ChequeListRetrieveSerializer(cheque)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.received_or_paid == Cheque.PAID:
            return Response(['چک پرداختی غیر قابل حذف می باشد'], status=status.HTTP_400_BAD_REQUEST)
        if instance.status != 'notPassed' or instance.statusChanges.count() != 1:
            return Response(['برای حذف چک باید ابتدا تغییر وضعیت های آن ها را پاک کنید'], status=status.HTTP_400_BAD_REQUEST)
        return super(ChequeModelView, self).perform_destroy(instance)

    def create(self, request, *args, **kwargs):
        request.data['financial_year'] = request.user.active_financial_year.id
        return super().create(request, *args, **kwargs)


class ChangeChequeStatus(APIView):
    # submit cheque
    def put(self, request, pk):
        queryset = Cheque.objects.inFinancialYear(request.user)
        cheque = get_object_or_404(queryset, pk=pk)

        statusChangesCount = cheque.statusChanges.count()
        if statusChangesCount != 0 and statusChangesCount != 1:
            return Response(['برای ویرایش چک باید ابتدا تغییر وضعیت های آن ها را پاک کنید'], status=status.HTTP_400_BAD_REQUEST)

        data = request.data['cheque']
        data['financial_year'] = request.user.active_financial_year.id

        if cheque.received_or_paid == Cheque.PAID:
            bank = cheque.chequebook.account.bank
            data['bankName'] = bank.name
            data['branchName'] = bank.branch
            data['accountNumber'] = bank.accountNumber
            data['serial'] = cheque.serial

        serialized = ChequeSerializer(cheque, data=data)
        if serialized.is_valid():
            serialized.save()
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data['statusChange']
        if cheque.received_or_paid == Cheque.RECEIVED:
            acc = getDA('receivedCheque', request.user).account
            data['bedAccount'] = acc.id
            cheque.lastAccount = acc
            # cheque.lastFloatAccount
            data['besAccount'] = cheque.account.id
            if cheque.floatAccount:
                data['besFloatAccount'] = cheque.floatAccount.id
        else:
            acc = getDA('paidCheque', request.user).account
            data['besAccount'] = acc.id
            cheque.lastAccount = acc
            # cheque.lastFloatAccount
            data['bedAccount'] = cheque.account.id
            if cheque.floatAccount:
                data['bedFloatAccount'] = cheque.floatAccount.id

        data['date'] = cheque.date
        data['cheque'] = cheque.id
        data['financial_year'] = request.user.active_financial_year.id
        data['fromStatus'] = 'blank'
        data['toStatus'] = 'notPassed'

        if 'update' in request.data and request.data['update']:
            serialized = StatusChangeSerializer(cheque.statusChanges.first(), data=data)
        else:
            serialized = StatusChangeSerializer(data=data)

        if serialized.is_valid():
            serialized.save()
            serialized.instance.createSanad(request.user)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        cheque.status = 'notPassed'
        cheque.save()

        return Response(serialized.data, status=status.HTTP_200_OK)

    # change cheque status
    def post(self, request, pk):
        data = request.data
        queryset = Cheque.objects.inFinancialYear(request.user)
        cheque = get_object_or_404(queryset, pk=pk)
        data['fromStatus'] = cheque.status
        data['financial_year'] = request.user.active_financial_year.id

        if cheque.received_or_paid == Cheque.RECEIVED:
            data['besAccount'] = cheque.lastAccount.id
            if cheque.lastFloatAccount:
                data['besFloatAccount'] = cheque.lastFloatAccount.id
            if data['toStatus'] == 'revoked' or data['toStatus'] == 'bounced':
                data['bedAccount'] = cheque.account.id
                if cheque.floatAccount:
                    data['bedFloatAccount'] = cheque.floatAccount.id
                else:
                    data.pop('bedFloatAccount', None)
        else:
            data['bedAccount'] = cheque.lastAccount.id
            if cheque.lastFloatAccount:
                data['bedFloatAccount'] = cheque.lastFloatAccount.id

            if data['toStatus'] == 'revoked' or data['toStatus'] == 'bounced':
                data['besAccount'] = cheque.account.id
                if cheque.floatAccount:
                    data['besFloatAccount'] = cheque.floatAccount.id

            if cheque.received_or_paid == Cheque.PAID and data['toStatus'] == 'passed':
                data['besAccount'] = cheque.chequebook.account.id
                if cheque.chequebook.floatAccount:
                    data['besFloatAccount'] = cheque.chequebook.floatAccount.id

        serialized = StatusChangeSerializer(data=data)
        if serialized.is_valid():
            if cheque.received_or_paid == Cheque.RECEIVED:
                cheque.lastAccount = Account.objects.inFinancialYear(request.user).get(pk=data['bedAccount'])
                if 'bedFloatAccount' in data:
                    cheque.lastFloatAccount = FloatAccount.objects.inFinancialYear(request.user).get(pk=data['bedFloatAccount'])
            else:
                cheque.lastAccount = Account.objects.inFinancialYear(request.user).get(pk=data['besAccount'])
                if 'besFloatAccount' in data:
                    cheque.lastFloatAccount = FloatAccount.objects.inFinancialYear(request.user).get(pk=data['besFloatAccount'])
            cheque.status = data['toStatus']
            cheque.save()
            serialized.save()
            serialized.instance.createSanad(request.user)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)


class StatusChangeView(generics.RetrieveDestroyAPIView):
    serializer_class = StatusChangeSerializer

    def get_queryset(self):
        return StatusChange.objects.inFinancialYear(self.request.user)


@api_view(['post'])
def revertChequeInFlowStatus(request, pk):
    queryset = Cheque.objects.inFinancialYear(request.user).all()
    cheque = get_object_or_404(queryset, pk=pk)
    if cheque.status != 'inFlow':
        return Response(['وضعیت چک باید درجریان باشد'], status.HTTP_400_BAD_REQUEST)
    statusChange = cheque.statusChanges.latest('id')
    if statusChange.toStatus != 'inFlow':
        # this should never happen
        return Response(['آخرین تغییر چک در جریان نمی باشد'], status.HTTP_400_BAD_REQUEST)
    data = request.data
    data['cheque'] = cheque.id
    data['fromStatus'] = 'inFlow'
    data['toStatus'] = statusChange.fromStatus
    data['bedAccount'] = statusChange.besAccount.id
    data['financial_year'] = request.user.active_financial_year.id
    if statusChange.besFloatAccount:
        data['bedFloatAccount'] = statusChange.besFloatAccount.id
    data['besAccount'] = statusChange.bedAccount.id
    if statusChange.bedFloatAccount:
        data['besFloatAccount'] = statusChange.bedFloatAccount

    serialized = StatusChangeSerializer(data=data)
    if serialized.is_valid():
        if cheque.received_or_paid == Cheque.RECEIVED:
            cheque.lastAccount = Account.objects.inFinancialYear(request.user).get(pk=data['bedAccount'])
            if 'bedFloatAccount' in data:
                cheque.lastFloatAccount = FloatAccount.objects.inFinancialYear(request.user).get(pk=data['bedFloatAccount'])
        else:
            cheque.lastAccount = Account.objects.inFinancialYear(request.user).get(pk=data['besAccount'])
            if 'besFloatAccount' in data:
                cheque.lastFloatAccount = FloatAccount.objects.inFinancialYear(request.user).get(pk=data['besFloatAccount'])
        cheque.status = data['toStatus']
        cheque.save()
        serialized.save()
        serialized.instance.createSanad(request.user)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serialized.data, status=status.HTTP_200_OK)


