from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from _dashtbashi.filters import OtherDriverPaymentFilter
from _dashtbashi.models import OtherDriverPayment
from _dashtbashi.report_views import LadingsReportView
from _dashtbashi.serializers import OtherDriverPaymentListRetrieveSerializer
from helpers.auth import BasicCRUDPermission
from reports.lists.export_views import BaseExportView, BaseListExportView


class LadingReportExportView(LadingsReportView, BaseListExportView):
    filename = 'ladings'
    pagination_class = None
    title = "لیست بارگیری ها"

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class OtherDriverPaymentFormExportView(ListAPIView, BaseExportView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'otherDriverPayment'
    serializer_class = OtherDriverPaymentListRetrieveSerializer
    filterset_class = OtherDriverPaymentFilter
    ordering_fields = '__all__'
    filename = 'other-driver-payment'

    context = {
        'title': 'پرداخت رانندگان متفرقه',
        'verifier_form_name': None
    }
    pagination_class = None

    def get_queryset(self):
        qs = OtherDriverPayment.objects.hasAccess(self.request.method)
        return self.filterset_class(self.request.GET, queryset=qs).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)


class OtherDriverPaymentListExportView(OtherDriverPaymentFormExportView, BaseListExportView):
    filename = 'other-driver-payments'
    title = "لیست پرداخت رانندگان متفرقه"

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)
