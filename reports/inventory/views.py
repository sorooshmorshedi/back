from django.db import connection
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from factors.models import FactorItem, Factor
from reports.inventory.serializers import FactorItemInventorySerializer
from wares.models import Ware


class InventoryListView(generics.ListAPIView):
    serializer_class = FactorItemInventorySerializer

    def get_queryset(self):
        return FactorItem.objects.inFinancialYear(self.request.user)

    def list(self, request, *args, **kwargs):
        if 'ware' not in request.GET or 'warehouse' not in request.GET:
            return Response(['choose a ware & warehouse'], status.HTTP_400_BAD_REQUEST)

        data = request.GET

        factor_items = self.get_queryset()\
            .filter(ware=data['ware'], warehouse=data['warehouse'])\
            .select_related('factor__account')\
            .select_related('factor__sanad')\
            .order_by('factor__date', 'factor__time')

        ware = Ware.objects.inFinancialYear(request.user).get(pk=data['ware'])
        output_fees = []
        # fifo
        if ware.pricingType == Ware.FIFO:
            for factorItem in factor_items:
                if factorItem.factor.type in ('buy', 'backFromSale'):
                    output_fees.append(
                        {
                            'fee': factorItem.fee,
                            'count': factorItem.count
                        }
                    )
        # avg
        elif ware.pricingType == Ware.WEIGHTED_MEAN:
            value_sum = 0
            count_sum = 0
            for factorItem in factor_items:
                if factorItem.factor.type in ('buy', 'backFromSale'):
                    value_sum += factorItem.fee * factorItem.count
                    count_sum += factorItem.count
            output_fees.append({
                'fee': value_sum/count_sum,
                'count': count_sum
            })

        remain_count = 0
        remain_total = 0
        for factorItem in factor_items:
            factorItem.input = None
            factorItem.output = None
            factorItem.remain = None
            if factorItem.factor.type in Factor.BUY_GROUP:
                remain_count += factorItem.count
                factorItem.input = {
                    'count': factorItem.count,
                    'fee': factorItem.fee,
                    'total': factorItem.count * factorItem.fee
                }
                remain_total += factorItem.input['total']
            else:
                remain_count -= factorItem.count
                total = 0
                count = factorItem.count
                while count != 0 and len(output_fees):
                    of = output_fees.pop()
                    if of['count'] == count:
                        total += count * of['fee']
                        count = 0
                    elif of['count'] > count:
                        total += count * of['fee']
                        of['count'] -= count
                        count = 0
                        output_fees.append(of)
                    else:
                        total += of['count'] * of['fee']
                        count -= of['count']
                factorItem.output = {
                    'count': factorItem.count,
                    'fee': '-',
                    'total': factorItem.count * factorItem.fee
                }
                remain_total -= factorItem.output['total']

            factorItem.remain = {
                'count': remain_count,
                'fee': remain_total / remain_count,
                'total': remain_total
            }

        res = FactorItemInventorySerializer(factor_items, many=True).data
        return Response(res, status.HTTP_200_OK)

