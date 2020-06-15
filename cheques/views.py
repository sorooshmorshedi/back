from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account, FloatAccount
from cheques.permissions import SubmitChequePermission, ChangeChequeStatusPermission
from cheques.serializers import *
from helpers.auth import BasicCRUDPermission
from sanads.models import clearSanad, Sanad


class ChequebookModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'chequebook'
    serializer_class = ChequebookCreateUpdateSerializer

    def get_queryset(self):
        return Chequebook.objects.inFinancialYear()

    def list(self, request, *ergs, **kwargs):
        queryset = self.get_queryset()
        serializer = ChequebookListRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        chequebook = get_object_or_404(queryset, pk=pk)
        serializer = ChequebookListRetrieveSerializer(chequebook)
        return Response(serializer.data)

    def perform_create(self, serializer: ChequeCreateUpdateSerializer):
        user = self.request.user
        serializer.save(
            code=Chequebook.newCode(user),
            financial_year=user.active_financial_year
        )

    def perform_destroy(self, instance: Chequebook):
        instance.is_deletable(raise_exception=True)
        super(ChequebookModelView, self).perform_destroy(instance)


"""
class ChequebookByPositionApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_base_codename = 'chequebook'

    def get(self, request):
        if 'position' not in request.GET or request.GET['position'] not in ('next', 'prev', 'first', 'last'):
            return Response(['موقعیت وارد نشده است'], status.HTTP_400_BAD_REQUEST)

        id = request.GET.get('id', None)
        position = request.GET['position']
        queryset = Chequebook.objects.inFinancialYear()

        try:
            if position == 'next':
                chequebook = queryset.filter(pk__gt=id).order_by('id')[0]
            elif position == 'prev':
                if id:
                    queryset = queryset.filter(pk__lt=id)
                chequebook = queryset.order_by('-id')[0]
            elif position == 'first':
                chequebook = queryset.order_by('id')[0]
            elif position == 'last':
                chequebook = queryset.order_by('-id')[0]
        except IndexError:
            return Response(['not found'], status=status.HTTP_404_NOT_FOUND)

        serializer = ChequebookListRetrieveSerializer(chequebook)
        return Response(serializer.data)
"""


class SubmitChequeApiView(APIView):
    permission_classes = (IsAuthenticated, SubmitChequePermission)
    serializer_class = ChequeCreateUpdateSerializer
    queryset = Cheque.objects.all()

    def get_queryset(self):
        return Cheque.objects.inFinancialYear()

    def post(self, request):

        user = self.request.user
        data = request.data

        cheque = self.submitCheque(user, data)

        return Response(ChequeListRetrieveSerializer(instance=cheque).data, status=status.HTTP_200_OK)

    @staticmethod
    def submitCheque(user, data):

        received_or_paid = data.get('received_or_paid')

        if received_or_paid == Cheque.RECEIVED:
            serializer = ChequeCreateUpdateSerializer(data=data)
        else:
            instance = get_object_or_404(Cheque, pk=data.get('id'))
            serializer = ChequeCreateUpdateSerializer(instance=instance, data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            status='blank',
        )

        cheque = serializer.instance

        sanad = Sanad.objects.inFinancialYear().filter(code=data.pop('sanad_code', None)).first()

        if sanad and not sanad.isEmpty:
            raise ValidationError("سند باید خالی باشد")

        status_change = cheque.changeStatus(
            user=user,
            date=cheque.date,
            to_status='notPassed',
            explanation=cheque.explanation,
            sanad=sanad
        )

        sanad = status_change.updateSanad(user)

        is_confirmed = data.get('_confirmed')
        if sanad and not is_confirmed:
            sanad.check_account_balance_confirmations()

        return cheque


def get_cheque_permission_base_codename(received_or_paid):
    if received_or_paid == Cheque.RECEIVED:
        return "receivedCheque"
    else:
        return "paidCheque"


class ChequeApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    queryset = Cheque.objects.all()
    serializer_class = ChequeListRetrieveSerializer

    @property
    def permission_base_codename(self):
        return get_cheque_permission_base_codename(self.get_object().received_or_paid)

    def update(self, request, *args, **kwargs):

        user = request.user
        cheque = self.get_object()

        serializer = ChequeCreateUpdateSerializer(instance=cheque, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            financial_year=user.active_financial_year,
            status='blank',
        )

        statusChanges = cheque.statusChanges.all()
        sanad = None
        if statusChanges.count() != 0:
            sanad = statusChanges.first().sanad

        statusChanges.delete()

        status_change = cheque.changeStatus(
            user=user,
            date=cheque.date,
            to_status='notPassed',
            explanation=cheque.explanation,
            sanad=sanad,
            account=cheque.account,
            floatAccount=cheque.floatAccount,
            costCenter=cheque.costCenter
        )
        sanad = status_change.updateSanad(user)

        is_confirmed = request.data.get('_confirmed')
        if not is_confirmed:
            sanad.check_account_balance_confirmations()

        return Response(ChequeListRetrieveSerializer(instance=cheque).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        cheque = self.get_object()

        if cheque.received_or_paid == Cheque.PAID:
            raise ValidationError("چک پرداختی غیر قابل حذف می باشد")

        if cheque.status != 'notPassed' or cheque.statusChanges.count() != 1:
            return Response(['برای حذف چک باید ابتدا تغییر وضعیت های آن ها را پاک کنید'],
                            status=status.HTTP_400_BAD_REQUEST)

        return super(ChequeApiView, self).destroy(request, *args, **kwargs)

    def perform_destroy(self, instance: Cheque):

        user = self.request.user
        if instance.has_transaction:
            transaction_item = instance.transactionItem
            transaction = transaction_item.transaction

            transaction_item.delete()
            transaction.updateSanad(user)
        else:
            status_change = instance.statusChanges.first()
            if status_change:
                sanad = status_change.sanad
                clearSanad(sanad)

        return super(ChequeApiView, self).perform_destroy(instance)


class ChequeByPositionApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_base_codename(self):
        received_or_paid = self.request.GET.get('received_or_paid')
        return get_cheque_permission_base_codename(received_or_paid)

    def get(self, request):
        if 'received_or_paid' not in request.GET:
            return Response(['نوع وارد نشده است'], status.HTTP_400_BAD_REQUEST)
        if 'position' not in request.GET or request.GET['position'] not in ('next', 'prev', 'first', 'last'):
            return Response(['موقعیت وارد نشده است'], status.HTTP_400_BAD_REQUEST)

        received_or_paid = request.GET['received_or_paid']
        id = request.GET.get('id', None)
        position = request.GET['position']
        queryset = Cheque.objects.inFinancialYear().filter(received_or_paid=received_or_paid)

        try:
            if position == 'next':
                cheque = queryset.filter(pk__gt=id).order_by('id')[0]
            elif position == 'prev':
                if id:
                    queryset = queryset.filter(pk__lt=id)
                cheque = queryset.order_by('-id')[0]
            elif position == 'first':
                cheque = queryset.order_by('id')[0]
            elif position == 'last':
                cheque = queryset.order_by('-id')[0]
        except IndexError:
            return Response(['not found'], status=status.HTTP_404_NOT_FOUND)

        serializer = ChequeListRetrieveSerializer(cheque)
        return Response(serializer.data)


class ChangeChequeStatus(APIView):
    permission_classes = (IsAuthenticated, ChangeChequeStatusPermission)

    def post(self, request, pk):
        user = request.user

        data = request.data
        queryset = Cheque.objects.inFinancialYear()
        cheque = get_object_or_404(queryset, pk=pk)

        date = data.get('date')
        to_status = data.get('to_status')
        account = Account.objects.filter(pk=data.get('account')).first()
        floatAccount = FloatAccount.objects.filter(pk=data.get('floatAccount')).first()
        costCenter = FloatAccount.objects.filter(pk=data.get('costCenter')).first()
        explanation = data.get('explanation')

        sanad = Sanad.objects.inFinancialYear().filter(code=data.pop('sanad_code', None)).first()

        if sanad and not sanad.isEmpty:
            raise ValidationError("سند باید خالی باشد")

        status_change = cheque.changeStatus(
            user=request.user,
            date=date,
            to_status=to_status,
            account=account,
            floatAccount=floatAccount,
            costCenter=costCenter,
            explanation=explanation,
            sanad=sanad
        )
        sanad = status_change.updateSanad(user)

        is_confirmed = data.get('_confirmed')
        if not is_confirmed:
            sanad.check_account_balance_confirmations()

        return Response(StatusChangeListRetrieveSerializer(instance=status_change).data, status=status.HTTP_200_OK)


class DeleteStatusChangeView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    serializer_class = StatusChangeSerializer

    @property
    def permission_base_codename(self):
        status_change = self.get_object()
        cheque = status_change.cheque
        if cheque.received_or_paid == Cheque.RECEIVED:
            return "receivedChequeStatusChange"
        else:
            return "paidChequeStatusChange"

    def get_queryset(self):
        return StatusChange.objects.inFinancialYear()

    def perform_destroy(self, instance: StatusChange):

        user = self.request.user
        cheque = instance.cheque

        last_status_change_id = StatusChange.objects.filter(cheque=cheque).latest('id').id

        if instance.id != last_status_change_id:
            raise serializers.ValidationError("ابتدا تغییرات جلوتر را پاک کنید")

        if cheque.statusChanges.count() == 1:
            if cheque.received_or_paid == Cheque.RECEIVED:
                raise ValidationError("حذف اولین تغییر وضعیت چک دریافتی امکان پذیر نیست")
            else:
                cheque.account = None
                cheque.floatAccount = None
                cheque.costCenter = None
                cheque.value = None
                cheque.due = None
                cheque.date = None
                cheque.explanation = ''
                cheque.lastAccount = None
                cheque.lastFloatAccount = None
                cheque.lastCostCenter = None

        if cheque.has_transaction:
            cheque.has_transaction = False
            transaction_item = cheque.transactionItem
            transaction_item.delete()
            transaction_item.transaction.updateSanad(user)
        else:
            clearSanad(instance.sanad)

        cheque.status = instance.fromStatus

        if cheque.received_or_paid == Cheque.RECEIVED:
            lastAccount = instance.besAccount
            lastFloatAccount = instance.besFloatAccount
            lastCostCenter = instance.besCostCenter
        else:
            lastAccount = instance.bedAccount
            lastFloatAccount = instance.bedFloatAccount
            lastCostCenter = instance.bedCostCenter

        cheque.lastAccount = lastAccount
        cheque.lastFloatAccount = lastFloatAccount
        cheque.lastCostCenter = lastCostCenter

        cheque.save()

        instance.delete()


class RevertChequeInFlowStatusView(APIView):
    permission_classes = (IsAuthenticated, ChangeChequeStatusPermission)

    def post(self, request, pk):
        queryset = Cheque.objects.inFinancialYear().all()
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
        if statusChange.besCostCenter:
            data['bedCostCenter'] = statusChange.besCostCenter.id
        data['besAccount'] = statusChange.bedAccount.id
        if statusChange.bedFloatAccount:
            data['besFloatAccount'] = statusChange.bedFloatAccount
        if statusChange.bedCostCenter:
            data['besCostCenter'] = statusChange.bedCostCenter

        serialized = StatusChangeSerializer(data=data)
        if serialized.is_valid():
            if cheque.received_or_paid == Cheque.RECEIVED:
                cheque.lastAccount = Account.objects.inFinancialYear().get(pk=data['bedAccount'])
                if 'bedFloatAccount' in data:
                    cheque.lastFloatAccount = FloatAccount.objects.inFinancialYear().get(
                        pk=data['bedFloatAccount'])
                if 'bedCostCenter' in data:
                    cheque.lastCostCenter = FloatAccount.objects.inFinancialYear().get(
                        pk=data['bedCostCenter'])

            else:
                cheque.lastAccount = Account.objects.inFinancialYear().get(pk=data['besAccount'])
                if 'besFloatAccount' in data:
                    cheque.lastFloatAccount = FloatAccount.objects.inFinancialYear().get(
                        pk=data['besFloatAccount'])
                if 'besCostCenter' in data:
                    cheque.lastCostCenter = FloatAccount.objects.inFinancialYear().get(
                        pk=data['besCostCenter'])

            cheque.status = data['toStatus']
            cheque.save()
            serialized.save()
            serialized.instance.createSanad(request.user)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)
