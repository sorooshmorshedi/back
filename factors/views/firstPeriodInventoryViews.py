from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account
from factors.models import Factor, FactorItem
from factors.serializers import FactorListRetrieveSerializer, FactorSerializer, FactorItemSerializer
from sanads.sanads.models import Sanad, newSanadCode, clearSanad


class FirstPeriodInventoryView(APIView):
    def get(self, request):
        factor = Factor.getFirstPeriodInventory(request.user)
        if not factor:
            return Response({'message': 'no first period inventory'}, status=status.HTTP_200_OK)
        serialized = FactorListRetrieveSerializer(factor)
        return Response(serialized.data)

    @transaction.atomic
    def post(self, request):

        if Factor.objects.inFinancialYear(request.user).filter(type__in=Factor.SALE_GROUP).count():
            return Response({'non_field_errors': ['لطفا ابتدا فاکتور های فروش و برگشت از خرید را حذف کنید']},
                            status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['factor'].pop('sanad', None)
        data['factor']['type'] = Factor.FIRST_PERIOD_INVENTORY
        data['factor']['is_definite'] = 1
        data['factor']['account'] = Account.get_partners_account(request.user).id
        data['factor']['financial_year'] = request.user.active_financial_year.id

        factor = Factor.getFirstPeriodInventory(request.user)
        if factor:
            serialized = FactorSerializer(instance=factor, data=data['factor'])
        else:
            serialized = FactorSerializer(data=data['factor'])

        serialized.is_valid(raise_exception=True)
        serialized.save()

        factor = serialized.instance
        factor.code = 0
        factor.save()

        items_to_create = []
        items_to_update = []

        SerializerClass = FactorItemSerializer

        for item in data.get('items', []):
            item['financial_year'] = request.user.active_financial_year.id
            if 'id' in item:
                items_to_update.append(item)
            else:
                items_to_create.append(item)

        for item in items_to_create:
            item['factor'] = factor.id

        serialized = SerializerClass(data=items_to_create, many=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        for item in items_to_update:
            instance = FactorItem.objects.inFinancialYear(request.user).get(id=item['id'])
            serialized = SerializerClass(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        ids_to_delete = data.get('ids_to_delete', [])
        if len(ids_to_delete):
            FactorItem.objects.inFinancialYear(request.user).filter(id__in=ids_to_delete).delete()

        for item in factor.items.all():
            item.total_input_count = item.count
            item.remain_value = item.value
            item.save()

        sanad = factor.sanad
        if not sanad:
            sanad = Sanad(code=newSanadCode(request.user), date=factor.date, explanation=factor.explanation,
                          createType=Sanad.AUTO, financial_year=request.user.active_financial_year)
            sanad.save()
            factor.sanad = sanad
            factor.save()

        if sanad.items.count():
            clearSanad(sanad)

        sanad.items.create(
            account=Account.get_inventory_account(request.user),
            value=factor.sum,
            valueType='bed',
            financial_year=request.user.active_financial_year
        )
        sanad.items.create(
            account=Account.get_partners_account(request.user),
            value=factor.sum,
            valueType='bes',
            financial_year=request.user.active_financial_year
        )

        res = Response(FactorSerializer(instance=factor).data, status=status.HTTP_200_OK)
        return res