from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from reports.ledger.filters import SanadItemLedgerFilter
from reports.ledger.serializers import SanadItemLedgerSerializer
from sanads.sanads.models import SanadItem


class LedgerListView(generics.ListAPIView):
    queryset = SanadItem.objects.order_by('sanad__code')
    serializer_class = SanadItemLedgerSerializer
    filterset_class = SanadItemLedgerFilter
    ordering_fields = ('sanad__date', 'sanad__code', 'explanation', 'account__code', 'account__name')
    pagination_class = LimitOffsetPagination

