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

        outputFees = []
        for r in rows:
            if r.factor.type in ('buy', 'backFromSale'):
                outputFees.append(
                    {
                        'fee': r.fee,
                        'count': r.count
                    }
                )

        remainCount = 0
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
            else:
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
            r.remain = {
                'count': remainCount,
                'fee': remainFee,
                'total': remainCount * remainFee
            }

        res = FactorItemInventorySerializer(rows, many=True).data
        return Response(res, status.HTTP_200_OK)

