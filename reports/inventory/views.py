from django.db import connection
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from factors.models import FactorItem, Factor
from factors.serializers import FactorItemSerializer
from reports.inventory.serializers import FactorItemInventorySerializer
from wares.models import Ware


class InventoryListView(generics.ListAPIView):
    serializer_class = FactorItemInventorySerializer

    def get_queryset(self):
        return FactorItem.objects.inFinancialYear(self.request.user).filter(factor__is_definite=True)

    def list(self, request, *args, **kwargs):
        if 'ware' not in request.GET or 'warehouse' not in request.GET:
            return Response(['choose a ware & warehouse'], status.HTTP_400_BAD_REQUEST)

        data = request.GET

        factor_items = self.get_queryset()\
            .filter(ware=data['ware'], warehouse=data['warehouse'])\
            .prefetch_related('factor__account')\
            .prefetch_related('factor__sanad')\
            .order_by('factor__definition_date')

        res = Response(FactorItemInventorySerializer(factor_items, many=True).data, status.HTTP_200_OK)
        return res

        ware = Ware.objects.inFinancialYear(request.user).get(pk=data['ware'])
        outputs = []
        total_remained_count = 0
        total_remained_value = 0
        for factorItem in factor_items:
            factorItem.input = None
            factorItem.output = None
            factorItem.remain = None
            if factorItem.factor.type in Factor.BUY_GROUP:
                total_remained_count += factorItem.count
                total_remained_value += factorItem.value
                outputs.append({
                    'fee': factorItem.fee,
                    'count': factorItem.count
                })
                factorItem.input = {
                    'count': factorItem.count,
                    'fee': factorItem.fee,
                    'total': factorItem.value
                }
            else:
                remained_count = factorItem.count
                total = 0
                if ware.pricingType == ware.FIFO:
                    fees = []
                    for output in outputs:
                        if remained_count == 0:
                            break
                        output_count = output['count']
                        output_fee = output['fee']
                        if output_count == 0:
                            continue
                        fee = {
                            'fee': output_fee,
                        }
                        if remained_count > output_count:
                            total += output_count * output_fee
                            fee['count'] = output_count
                            output['count'] = 0
                            remained_count -= output_count
                        else:
                            total += remained_count * output_fee
                            fee['count'] = remained_count
                            output['count'] -= remained_count
                            remained_count = 0

                        fees.append(fee)

                    total_remained_value -= total
                    factorItem.output = {
                        'count': factorItem.count,
                        'fees': fees,
                        'total': total
                    }
                else:
                    fee = total_remained_value / total_remained_count
                    total = fee * factorItem.count
                    total_remained_value -= total
                    factorItem.output = {
                        'count': factorItem.count,
                        'fee': fee,
                        'total': total
                    }

                total_remained_count -= factorItem.count

            factorItem.remain = {
                'count': total_remained_count,
                'fee': "{0:.2f}".format(total_remained_value / total_remained_count) if ware.pricingType == ware.WEIGHTED_MEAN else '-',
                'total': total_remained_value

            }

        res = FactorItemInventorySerializer(factor_items, many=True).data
        return Response(res, status.HTTP_200_OK)

