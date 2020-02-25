from django.http import HttpResponse
from import_export.fields import Field
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from reports.journal.filters import SanadItemJounalFilter
from reports.journal.serializers import SanadItemJournalSerializer
from reports.views import ModelResource
from sanads.sanads.models import SanadItem


class SanadItemResource(ModelResource):
    بدهکار = Field()
    بستانکار = Field()

    class Meta:
        model = SanadItem
        fields = ('sanad__date', 'sanad__code', 'explanation', 'account__code', 'account__name')

    def dehydrate_بدهکار(self, sanadItem):
        return sanadItem.bed

    def dehydrate_بستانکار(self, sanadItem):
        return sanadItem.bes


class JournalListView(generics.ListAPIView):
    serializer_class = SanadItemJournalSerializer
    filterset_class = SanadItemJounalFilter
    ordering_fields = ('sanad__date', 'sanad__code', 'explanation', 'account__code', 'account__name', 'bed', 'bes')
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return SanadItem.objects.inFinancialYear(self.request.user).all()

    def list(self, request, *args, **kwargs):

        if 'download' in request.GET and request.GET['download'] == 'xls':
            f = self.filterset_class(request.GET, queryset=self.queryset)
            dataset = SanadItemResource().export(f.qs)
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="persons.xls"'
            return response
        else:
            return super(JournalListView, self).list(request)

