import jdatetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account
from factors.models import Factor
from factors.serializers import FactorListRetrieveSerializer, FactorCreateUpdateSerializer, FactorItemSerializer
from factors.views.definite_factor import DefiniteFactor
from helpers.auth import BasicCRUDPermission
from helpers.functions import get_current_user, get_object_accounts
from helpers.views.MassRelatedCUD import MassRelatedCUD
from sanads.models import Sanad, newSanadCode, clearSanad


class FirstPeriodInventoryItemMassRelatedCUD(MassRelatedCUD):

    def perform_create(self, serializer):
        serializer.save(
            financial_year=self.financial_year
        )

    def perform_update(self, serializer):
        serializer.save(
            financial_year=self.financial_year
        )


class FirstPeriodInventoryView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = 'get.firstPeriodInventory'

    def get(self, request):
        factor = Factor.get_first_period_inventory()
        if not factor:
            return Response({'message': 'no first period inventory'}, status=status.HTTP_200_OK)
        serialized = FactorListRetrieveSerializer(factor)
        return Response(serialized.data)

    @staticmethod
    def set_first_period_inventory(data, financial_year=None, engage_inventory=True, submit_sanad=True,
                                   is_auto_created=False):
        """
        :param submit_sanad:
        :param engage_inventory:
        :param is_auto_created:
        :param data: {
            item: {...},
            items: {
                items: [{..}, ...},
                ids_to_delete: []
        }
        :param financial_year:
        :return:
        """

        user = get_current_user()

        if not financial_year:
            financial_year = user.active_financial_year

        factor_data = data['item']
        factor_items_data = data.get('items')

        first_period_inventory = Factor.get_first_period_inventory(financial_year)
        if first_period_inventory:
            DefiniteFactor.updateFactorInventory(first_period_inventory, True)
            first_period_inventory.is_defined = True
            first_period_inventory.is_auto_created = is_auto_created
            first_period_inventory.code = 0
            first_period_inventory.save()

        first_period_inventory = FirstPeriodInventoryView._create_or_update_factor(
            factor_data,
            factor_items_data,
            financial_year,
            user,
            engage_inventory
        )

        if submit_sanad:
            sanad = FirstPeriodInventoryView._create_or_update_sanad(first_period_inventory, financial_year, user)
            is_confirmed = data.get('_confirmed')
            if not is_confirmed:
                sanad.check_account_balance_confirmations()
        else:
            sanad = first_period_inventory.sanad
            if sanad:
                clearSanad(sanad)
                first_period_inventory.sanad = None
                first_period_inventory.save()

        return first_period_inventory

    @staticmethod
    def _create_or_update_factor(factor_data, factor_items_data, financial_year, user, engage_inventory=True):
        factor_data.pop('sanad', None)
        factor_data['type'] = Factor.FIRST_PERIOD_INVENTORY
        factor_data['is_defined'] = 1

        first_period_inventory = Factor.get_first_period_inventory(financial_year)
        if first_period_inventory:
            if engage_inventory:
                first_period_inventory.verify_items(factor_items_data['items'], factor_items_data['ids_to_delete'])
            serializer = FactorCreateUpdateSerializer(instance=first_period_inventory, data=factor_data)
        else:
            serializer = FactorCreateUpdateSerializer(data=factor_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(
            code=0,
            temporary_code=0,
            financial_year=financial_year
        )

        if not first_period_inventory:
            first_period_inventory = serializer.instance
            first_period_inventory.definition_date = str(jdatetime.date.today())
            first_period_inventory.save()
            if engage_inventory:
                first_period_inventory.verify_items(factor_items_data['items'], factor_items_data['ids_to_delete'])

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

        first_period_inventory.refresh_from_db()

        for item in first_period_inventory.items.all():
            item.save()

        if engage_inventory:
            DefiniteFactor.updateFactorInventory(first_period_inventory)

        return first_period_inventory

    @staticmethod
    def _create_or_update_sanad(first_period_inventory, financial_year, user):
        sanad = first_period_inventory.sanad
        if not sanad:
            sanad = Sanad(code=newSanadCode(financial_year), date=first_period_inventory.date,
                          explanation=first_period_inventory.explanation,
                          financial_year=financial_year)
            sanad.save()
            first_period_inventory.sanad = sanad
            first_period_inventory.save()

        if sanad.items.count():
            clearSanad(sanad)
            sanad.is_auto_created = True

        sanad.items.create(
            account=Account.get_inventory_account(user),
            bed=first_period_inventory.sum,
            financial_year=financial_year,
        )
        sanad.items.create(
            **get_object_accounts(first_period_inventory),
            bes=first_period_inventory.sum,
            financial_year=financial_year,
        )

        return sanad
