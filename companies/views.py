from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account
from accounts.defaultAccounts.models import getDA
from companies.models import Company, FinancialYear
from rest_framework import generics

from companies.permissions import CompanyListCreate, CompanyDetail
from companies.serializers import CompanySerializer, FinancialYearSerializer
from sanads.sanads.models import SanadItem, newSanadCode, Sanad
from sanads.sanads.serializers import SanadSerializer, SanadItemSerializer


@method_decorator(csrf_exempt, name='dispatch')
class CompanyModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, CompanyListCreate,)
    queryset = Company.objects.prefetch_related('financial_years').all()
    serializer_class = CompanySerializer


class FinancialYearModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer


class CloseAccountsView(APIView):
    user = None
    accounts = None
    created_sanads = []

    def post(self, request):
        self.user = request.user
        self.resetAccounts()
        self.closeTemporaries()
        self.closeEarnings()
        self.closePermanents()
        self.closeNeutrals()
        return Response({}, status=status.HTTP_200_OK)

    def closeTemporaries(self):
        explanation = 'بابت بستن حساب های موقت'
        account = getDA('currentEarnings', self.user).account
        self.createSanad(6, account, explanation)
        self.createSanad(7, account, explanation)
        self.createSanad(8, account, explanation)

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
        self.createSanad(1, account, explanation)
        self.createSanad(2, account, explanation)
        self.createSanad(3, account, explanation)
        self.createSanad(4, account, explanation)
        self.createSanad(5, account, explanation)

        remain = account.get_remain()
        if remain['value'] != 0:
            raise ValidationError(detail='حساب اختتامیه مانده دارد')

    def closeNeutrals(self):
        explanation = 'بابت بستن حساب ها'
        items = []
        sanad_bed_sum = 0
        sanad_bes_sum = 0
        for account in self.accounts:
            if account.code.find('9') != 0:
                continue
            if account.bed_sum == account.bes_sum == 0:
                continue

            sanad_bed_sum += account.bed_sum
            sanad_bes_sum += account.bes_sum

            if account.bed_sum == 0:
                value_type = SanadItem.BES
                value = account.bes_sum
            else:
                value_type = SanadItem.BED
                value = account.bed_sum

            items.append({
                'account': account.id,
                'value': value,
                'valueType': value_type,
            })

        if sanad_bes_sum - sanad_bed_sum == 0:
            self.saveSanad(items, explanation)
        else:
            raise ValidationError(detail='سند بستن حساب های خنتی تراز نیست')

    def createSanad(self, code, destination_account, explanation):
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

            value_type = SanadItem.BED
            value = account.bed_sum - account.bes_sum
            if value < 0:
                value_type = SanadItem.BES
                value = -value

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

        items.append({
            'account': destination_account.id,
            'value': sanad_remain,
            'valueType': sanad_value_type,
        })

        if sanad_remain != 0:
            self.saveSanad(items, explanation)

    def saveSanad(self, items, explanation):
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
            .prefetch_related('floatAccountGroup')

