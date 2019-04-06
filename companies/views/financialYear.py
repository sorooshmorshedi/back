from django.db import connection
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account
from accounts.defaultAccounts.models import getDA
from sanads.sanads.models import SanadItem, newSanadCode, Sanad
from sanads.sanads.serializers import SanadSerializer, SanadItemSerializer


class ClosingBaseView(APIView):
    user = None
    accounts = None
    created_sanads = []

    TemporaryGroupCodes = [6, 7, 8]
    PermanentGroupCodes = [1, 2, 3, 4, 5]
    NeuralGroupCode = 9

    def createSanad(self, code, destination_account, explanation):
        res = self.createSanadItems(code, destination_account)
        items = res['items']
        sanad_remain = res['sanad_remain']
        if sanad_remain != 0:
            self.saveSanad(items, explanation)

    # By default reverses valueTypes
    def createSanadItems(self, code, destination_account):
        # todo FloatAccounts
        items = []
        sanad_bed_sum = 0
        sanad_bes_sum = 0
        for account in self.accounts:
            if account.code.find(str(code)) != 0:
                continue
            if account.bed_sum == account.bes_sum == 0:
                continue

            sanad_bed_sum += account.bed_sum
            sanad_bes_sum += account.bes_sum

            value = account.bed_sum - account.bes_sum
            if value < 0:
                value_type = SanadItem.BES
                value = -value
            else:
                value_type = SanadItem.BED

            items.append({
                'account': account.id,
                'value': value,
                'valueType': value_type,
            })

        sanad_remain = sanad_bed_sum - sanad_bes_sum
        sanad_value_type = SanadItem.BES
        if sanad_remain < 0:
            sanad_remain = -sanad_remain
            sanad_value_type = SanadItem.BED

        if destination_account:
            items.append({
                'account': destination_account.id,
                'value': sanad_remain,
                'valueType': sanad_value_type,
            })

        return {
            'items': items,
            'sanad_remain': sanad_remain
        }

    def saveSanad(self, items, explanation, financial_year=None):
        if not financial_year:
            financial_year = self.user.active_financial_year
        data = {
            'financial_year': financial_year.id,
            'date': financial_year.end,
            'code': newSanadCode(self.user),
            'explanation': explanation,
            'type': Sanad.TEMPORARY,
            'createType': Sanad.AUTO
        }
        serialized = SanadSerializer(data=data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        sanad = serialized.instance
        self.created_sanads.append(sanad)

        for item in items:
            item['explanation'] = explanation
            item['financial_year'] = financial_year.id
            item['sanad'] = sanad.id
        serialized = SanadItemSerializer(data=items, many=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

    def resetAccounts(self):
        self.accounts = Account.objects.inFinancialYear(self.user) \
            .filter(level=Account.TAFSILI) \
            .annotate(bed_sum=Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bed')), 0)) \
            .annotate(bes_sum=Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bes')), 0)) \
            .prefetch_related('sanadItems') \
            .prefetch_related('floatAccountGroup')

    @staticmethod
    def getReversedSanadItems(items):
        new_items = []
        for item in items:
            new_item = item.copy()
            if new_item['valueType'] == SanadItem.BED:
                new_item['valueType']= SanadItem.BES
            else:
                new_item['valueType'] = SanadItem.BED
            new_items.append(new_item)
        return new_items


class CloseAccountsView(ClosingBaseView):

    def post(self, request):
        self.user = request.user
        self.resetAccounts()
        # self.openingSanad(self.user.active_financial_year)
        # print(len(connection.queries))
        # return Response({}, status=status.HTTP_200_OK)
        self.closeTemporaries()
        self.closeEarnings()
        self.closePermanents()
        self.closeNeutrals()
        return Response({}, status=status.HTTP_200_OK)

    def closeTemporaries(self):
        explanation = 'بابت بستن حساب های موقت'
        account = getDA('currentEarnings', self.user).account
        for code in self.TemporaryGroupCodes:
            self.createSanad(code, account, explanation)

    def closeEarnings(self):
        self.resetAccounts()
        explanation = 'بابت بستن حساب سود و زیان جاری'
        account = getDA('currentEarnings', self.user).account
        remain = account.get_remain()
        destination_account = getDA('retainedEarnings', self.user).account

        items = []
        value = remain['value']
        if remain['remain_type'] == SanadItem.BED:
            value_type = SanadItem.BES
        else:
            value_type = SanadItem.BED

        items.append({
            'account': account.id,
            'value': value,
            'valueType': value_type,
        })

        if value_type == SanadItem.BED:
            value_type = SanadItem.BES
        else:
            value_type = SanadItem.BED

        items.append({
            'account': destination_account.id,
            'value': value,
            'valueType': value_type,
        })

        if value != 0:
            self.saveSanad(items, explanation)

    def closePermanents(self):
        self.resetAccounts()
        explanation = 'بابت بستن حساب های دائمی'
        account = getDA('closing', self.user).account
        for code in self.PermanentGroupCodes:
            self.createSanad(code, account, explanation)

        remain = account.get_remain()
        if remain['value'] != 0:
            raise ValidationError(detail='حساب اختتامیه مانده دارد')

    def closeNeutrals(self):
        explanation = 'بابت بستن حساب ها'
        res = self.createSanadItems(self.NeuralGroupCode, destination_account=None)
        items = res['items']
        sanad_remain = res['sanad_remain']

        if sanad_remain == 0:
            if len(items):
                self.saveSanad(items, explanation)
        else:
            raise ValidationError(detail='سند بستن حساب های خنتی تراز نیست')

    def openingSanad(self, financial_year):
        explanation = 'بابت افتتاح حساب'
        account = getDA('closing', self.user).account
        items = []
        for code in self.PermanentGroupCodes:
            res = self.createSanadItems(code, account)
            items += res['items']
        res = self.createSanadItems(self.NeuralGroupCode, destination_account=None)
        items += res['items']
        items = self.getReversedSanadItems(items)
        self.saveSanad(items, explanation, financial_year)


class MoveAccountsView(ClosingBaseView):
    def post(self, request):
        self.user = request.user
        self.resetAccounts()
        return Response({}, status=status.HTTP_200_OK)