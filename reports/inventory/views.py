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
