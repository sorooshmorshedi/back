from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from reports.journal.filters import SanadItemJounalFilter
from reports.journal.serializers import SanadItemJournalSerializer
from sanads.sanads.models import SanadItem


class JournalListView(generics.ListAPIView):
    queryset = SanadItem.objects.all()
    serializer_class = SanadItemJournalSerializer
    filterset_class = SanadItemJounalFilter
    ordering_fields = ('sanad__date', 'sanad__code', 'explanation', 'account__code', 'account__name', 'value', 'valueType')
    pagination_class = LimitOffsetPagination

