from django.db import connection
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from factors.models import FactorItem
from reports.inventory.serializers import FactorItemInventorySerializer
from wares.models import Ware


class InventoryListView(generics.ListAPIView):
    serializer_class = FactorItemInventorySerializer

    queryset = FactorItem.objects

    def list(self, request, *args, **kwargs):
        if 'ware' not in request.GET or 'warehouse' not in request.GET:
            return Response(['choose a ware & warehouse'], status.HTTP_400_BAD_REQUEST)

        data = request.GET

        rows = self.queryset\
            .filter(ware=data['ware'], warehouse=data['warehouse'])\
            .select_related('factor__account') \
            .select_related('factor__sanad')\
            .order_by('-factor__date', '-factor__time')

        ware = Ware.objects.get(pk=data['ware'])
        outputFees = []
        if ware.pricingType == 0: #fifo
            for r in rows:
                if r.factor.type in ('buy', 'backFromSale'):
                    outputFees.append(
                        {
                            'fee': r.fee,
                            'count': r.count
                        }
                    )
        elif ware.pricingType == 1: #avg
            valueSum = 0
            countSum = 0
            for r in rows:
                if r.factor.type in ('buy', 'backFromSale'):
                    valueSum += r.fee * r.count
                    countSum += r.count
            outputFees.append({
                'fee': valueSum/countSum,
                'count': countSum
            })

        remainCount = 0
        remainTotal = 0
        remainFee = 0
        for r in rows:
            r.input = None
            r.output = None
            r.remain = None
            if r.factor.type in ('buy', 'backFromSale'):
                remainCount += r.count
                r.input = {
                    'count': r.count,
                    'fee': r.fee,
                    'total': r.count * r.fee
                }
                remainTotal += r.input['total']
            else:
                remainCount -= r.count
                total = 0
                count = r.count
                while count != 0:
                    of = outputFees.pop()
                    if of['count'] == count:
                        total += count * of['fee']
                        count = 0
                    elif of['count'] > count:
                        total += count * of['fee']
                        of['count'] -= count
                        count = 0
                        outputFees.append(of)
                    else:
                        total += of['count'] * of['fee']
                        count -= of['count']
                r.output = {
                    'count': r.count,
                    'fee': r.fee,
                    'total': r.count * r.fee
                }
                remainTotal -= r.output['total']

            r.remain = {
                'count': remainCount,
                'fee': remainTotal / remainCount,
                'total': remainTotal
            }

        res = FactorItemInventorySerializer(rows, many=True).data
        return Response(res, status.HTTP_200_OK)

