from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account, FloatAccount
from cheques.serializers import *
from sanads.sanads.models import clearSanad


class ChequebookModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChequebookCreateUpdateSerializer

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

    def perform_create(self, serializer: ChequeCreateUpdateSerializer):
        user = self.request.user
        serializer.save(
            code=Chequebook.newCode(user),
            financial_year=user.active_financial_year
        )

    def perform_destroy(self, instance: Chequebook):
        instance.is_deletable(raise_exception=True)
        super(ChequebookModelView, self).perform_destroy(instance)


class ChequebookByPositionApiView(APIView):

    def get(self, request):
        if 'position' not in request.GET or request.GET['position'] not in ('next', 'prev', 'first', 'last'):
            return Response(['موقعیت وارد نشده است'], status.HTTP_400_BAD_REQUEST)

        id = request.GET.get('id', None)
        position = request.GET['position']
        queryset = Chequebook.objects.inFinancialYear(request.user)

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


class SubmitChequeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChequeCreateUpdateSerializer
    queryset = Cheque.objects.all()

    def get_queryset(self):
        return Cheque.objects.inFinancialYear(self.request.user)

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

        status_change = cheque.changeStatus(
            user=user,
            date=cheque.date,
            to_status='notPassed',
            explanation=cheque.explanation,
        )

        sanad = status_change.updateSanad(user)

        is_confirmed = data.get('_confirmed')
        if sanad and not is_confirmed:
            sanad.check_account_balance_confirmations()

        return cheque


class ChequeApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cheque.objects.all()
    serializer_class = ChequeListRetrieveSerializer

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
            sanad=sanad
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

    def get(self, request):
        if 'received_or_paid' not in request.GET:
            return Response(['نوع وارد نشده است'], status.HTTP_400_BAD_REQUEST)
        if 'position' not in request.GET or request.GET['position'] not in ('next', 'prev', 'first', 'last'):
            return Response(['موقعیت وارد نشده است'], status.HTTP_400_BAD_REQUEST)

        received_or_paid = request.GET['received_or_paid']
        id = request.GET.get('id', None)
        position = request.GET['position']
        queryset = Cheque.objects.inFinancialYear(request.user).filter(received_or_paid=received_or_paid)

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
    def post(self, request, pk):
        user = request.user

        data = request.data
        queryset = Cheque.objects.inFinancialYear(request.user)
        cheque = get_object_or_404(queryset, pk=pk)

        date = data.get('date')
        to_status = data.get('to_status')
        account = get_object_or_404(Account, pk=data.get('account'))
        floatAccount = FloatAccount.objects.filter(pk=data.get('floatAccount')).first()
        explanation = data.get('explanation')

        status_change = cheque.changeStatus(
            user=request.user,
            date=date,
            to_status=to_status,
            account=account,
            floatAccount=floatAccount,
            explanation=explanation,
        )
        sanad = status_change.updateSanad(user)

        is_confirmed = data.get('_confirmed')
        if not is_confirmed:
            sanad.check_account_balance_confirmations()

        return Response(StatusChangeListRetrieveSerializer(instance=status_change).data, status=status.HTTP_200_OK)


class StatusChangeView(generics.RetrieveDestroyAPIView):
    serializer_class = StatusChangeSerializer

    def get_queryset(self):
        return StatusChange.objects.inFinancialYear(self.request.user)

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
                cheque.value = None
                cheque.due = None
                cheque.date = None
                cheque.explanation = ''
                cheque.lastAccount = None
                cheque.lastFloatAccount = None

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
        else:
            lastAccount = instance.bedAccount
            lastFloatAccount = instance.bedFloatAccount

        cheque.lastAccount = lastAccount
        cheque.lastFloatAccount = lastFloatAccount

        cheque.save()

        instance.delete()


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
                cheque.lastFloatAccount = FloatAccount.objects.inFinancialYear(request.user).get(
                    pk=data['bedFloatAccount'])
        else:
            cheque.lastAccount = Account.objects.inFinancialYear(request.user).get(pk=data['besAccount'])
            if 'besFloatAccount' in data:
                cheque.lastFloatAccount = FloatAccount.objects.inFinancialYear(request.user).get(
                    pk=data['besFloatAccount'])
        cheque.status = data['toStatus']
        cheque.save()
        serialized.save()
        serialized.instance.createSanad(request.user)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serialized.data, status=status.HTTP_200_OK)
