from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account
from factors.models import Factor
from factors.serializers import FactorListRetrieveSerializer, FactorCreateUpdateSerializer, FactorItemSerializer
from factors.views.factorViews import DefiniteFactor
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_current_user
from helpers.views.MassRelatedCUD import MassRelatedCUD
from sanads.models import Sanad, newSanadCode, clearSanad


class FirstPeriodInventoryItemMassRelatedCUD(MassRelatedCUD):

    def perform_create(self, serializer):
        serializer.save(
            financial_year=self.financial_year
        )
        for item in serializer.instance:
            DefiniteFactor.updateInventoryOnFactorItemSave(item, self.financial_year)

    def perform_update(self, serializer):
        serializer.save(
            financial_year=self.financial_year
        )
        DefiniteFactor.updateInventoryOnFactorItemSave(serializer.instance, self.financial_year)


class FirstPeriodInventoryView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'firstPeriodInventory'

    def get(self, request):
        factor = Factor.get_first_period_inventory()
        if not factor:
            return Response({'message': 'no first period inventory'}, status=status.HTTP_200_OK)
        serialized = FactorListRetrieveSerializer(factor)
        return Response(serialized.data)

    def post(self, request):

        if Factor.objects.inFinancialYear().filter(type__in=Factor.SALE_GROUP).count():
            return Response({'non_field_errors': ['لطفا ابتدا فاکتور های فروش و برگشت از خرید را حذف کنید']},
                            status=status.HTTP_400_BAD_REQUEST)

        first_period_inventory = self.set_first_period_inventory(request.data)

        res = Response(FactorListRetrieveSerializer(instance=first_period_inventory).data, status=status.HTTP_200_OK)
        return res

    @staticmethod
    def set_first_period_inventory(data, financial_year=None):
        """
        :param data: {
            factor: {...},
            factor_items: {
                items: [{..}, ...},
                ids_to_delete: []
        }
        :param financial_year:
        :return:
        """

        user = get_current_user()

        if not financial_year:
            financial_year = user.active_financial_year

        factor_data = data['factor']
        factor_items_data = data.get('factor_items')

        first_period_inventory = Factor.get_first_period_inventory(financial_year)
        if first_period_inventory:
            DefiniteFactor.undoDefinition(user, first_period_inventory)

        first_period_inventory = FirstPeriodInventoryView._create_or_update_factor(factor_data, factor_items_data,
                                                                                   financial_year, user)

        sanad = FirstPeriodInventoryView._create_or_update_sanad(first_period_inventory, financial_year, user)

        is_confirmed = data.get('_confirmed')
        if not is_confirmed:
            sanad.check_account_balance_confirmations()

        return first_period_inventory

    @staticmethod
    def _create_or_update_factor(factor_data, factor_items_data, financial_year, user):
        factor_data.pop('sanad', None)
        factor_data['type'] = Factor.FIRST_PERIOD_INVENTORY
        factor_data['is_definite'] = 1
        factor_data['account'] = Account.get_partners_account(user).id

        first_period_inventory = Factor.get_first_period_inventory(financial_year)
        if first_period_inventory:
            serializer = FactorCreateUpdateSerializer(instance=first_period_inventory, data=factor_data)
        else:
            serializer = FactorCreateUpdateSerializer(data=factor_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(
            code=0,
            financial_year=financial_year
        )

        first_period_inventory = serializer.instance

        FirstPeriodInventoryItemMassRelatedCUD(
            user,
            factor_items_data.get('items', []),
            factor_items_data.get('ids_to_delete', []),
            'factor',
            first_period_inventory.id,
            FactorItemSerializer,
            FactorItemSerializer,
            financial_year=financial_year
        ).sync()

        for item in first_period_inventory.items.all():
            item.save()

        return first_period_inventory

    @staticmethod
    def _create_or_update_sanad(first_period_inventory, financial_year, user):
        sanad = first_period_inventory.sanad
        if not sanad:
            sanad = Sanad(code=newSanadCode(financial_year), date=first_period_inventory.date,
                          explanation=first_period_inventory.explanation,
                          createType=Sanad.AUTO, financial_year=financial_year)
            sanad.save()
            first_period_inventory.sanad = sanad
            first_period_inventory.save()

        if sanad.items.count():
            clearSanad(sanad)

        sanad.items.create(
            account=Account.get_inventory_account(user),
            bed=first_period_inventory.sum,
            financial_year=financial_year
        )
        sanad.items.create(
            account=Account.get_partners_account(user),
            bes=first_period_inventory.sum,
            financial_year=financial_year
        )

        return sanad
