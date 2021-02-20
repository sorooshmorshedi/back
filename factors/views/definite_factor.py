import datetime

from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from factors.factor_sanad import FactorSanad
from factors.models import Factor
from factors.models.factor import FactorItem, get_factor_permission_basename
from helpers.auth import BasicCRUDPermission
from wares.models import WareInventory


class DefiniteFactor(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    @property
    def permission_codename(self):
        if self.request.method.lower() == 'post' and 'item' in self.request.data:
            factor_data = self.request.data['item']
            factor_type = factor_data.get('type')
        else:
            factor_type = Factor.objects.get(pk=self.kwargs['pk']).type

        return "definite.{}".format(get_factor_permission_basename(factor_type))

    def post(self, request, pk):
        user = request.user
        factor = DefiniteFactor.definiteFactor(user, pk, is_confirmed=request.data.get('_confirmed'))
        from factors.serializers import FactorListRetrieveSerializer
        return Response(FactorListRetrieveSerializer(factor).data)

    @staticmethod
    def definiteFactor(user, pk, is_confirmed=False):
        factor = get_object_or_404(Factor.objects.inFinancialYear(), pk=pk)

        if factor.type == Factor.FIRST_PERIOD_INVENTORY:
            factor.temporary_code = 0
            factor.code = 0
        else:
            factor.code = Factor.get_new_code(factor_type=factor.type)

        factor.is_definite = True

        if factor.financial_year.is_advari:
            factor.definition_date = datetime.datetime.combine(factor.date.togregorian(), factor.time)
        elif not factor.definition_date:
            factor.definition_date = now()

        factor.save()

        DefiniteFactor.updateFactorInventory(factor)

        FactorSanad(factor).update(is_confirmed)

        return factor

    @staticmethod
    def updateFactorInventory(factor: Factor, revert=False):
        for item in factor.items.order_by('id').all():
            DefiniteFactor._updateInventory(item, revert)

    @staticmethod
    def _updateInventory(item: FactorItem, revert):

        factor = item.factor
        ware = item.ware
        warehouse = item.warehouse

        if item.ware.is_service:
            return

        if not item.financial_year.is_advari:
            usage_in_next_years = FactorItem.objects.filter(
                factor__financial_year__start__gt=factor.financial_year.end,
                factor__financial_year__company=factor.financial_year.company,
                factor__type__in=Factor.OUTPUT_GROUP,
                ware=ware
            )

            if usage_in_next_years.exists():
                raise ValidationError("ابتدا فاکتور های سال مالی بعدی را پاک نمایید")

        if not revert:
            if factor.type in Factor.OUTPUT_GROUP:
                fees = WareInventory.decrease_inventory(ware, warehouse, item.count, factor.financial_year)
                item.fees = fees
                item.save()

            elif factor.type in Factor.INPUT_GROUP:
                fee = item.fee
                if factor.type == Factor.BACK_FROM_SALE:
                    fee = float(WareInventory.get_remain_fees(ware, warehouse)[-1]['fee'])
                item.fees = [{
                    'fee': float(fee),
                    'count': float(item.count)
                }]
                item.save()
                WareInventory.increase_inventory(ware, warehouse, item.count, fee, factor.financial_year)

            item.remain_fees = WareInventory.get_remain_fees(item.ware, item.warehouse)

        else:
            if item.factor.type in Factor.INPUT_GROUP:
                WareInventory.decrease_inventory(ware, warehouse, item.count, factor.financial_year, revert=True)
            else:
                fees = item.fees.copy()
                fees.reverse()
                for fee in fees:
                    WareInventory.increase_inventory(
                        ware,
                        warehouse,
                        fee['count'],
                        fee['fee'],
                        factor.financial_year,
                        revert=True
                    )

            item.fees = []
            item.remain_fees = []

        item.save()
