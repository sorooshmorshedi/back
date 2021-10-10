from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from _dashtbashi.filters import OtherDriverPaymentFilter
from _dashtbashi.models import OtherDriverPayment, Car, OilCompanyLading
from _dashtbashi.report_views import LadingListView, LadingBillSeriesListView, RemittanceListView, \
    OilCompanyLadingListView, OilCompanyLadingItemListView
from _dashtbashi.serializers import OtherDriverPaymentListRetrieveSerializer
from _dashtbashi.views import LadingBillNumberListView
from helpers.auth import BasicCRUDPermission
from reports.lists.export_views import BaseExportView, BaseListExportView


class LadingListExportView(LadingListView, BaseListExportView):
    filename = 'ladings'
    title = None

    def get_rows(self):
        return self.filterset_class(self.request.GET, queryset=self.get_queryset()).qs.all()

    def get(self, request, *args, **kwargs):
        self.title = request.GET.get('title', 'لیست بارگیری ها')
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
        qs = OtherDriverPayment.objects.hasAccess(self.request.method).filter(driving__car__owner=Car.OTHER)
        return self.filterset_class(self.request.GET, queryset=qs).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)


class OtherDriverPaymentListExportView(ListAPIView, BaseListExportView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'otherDriverPayment'
    serializer_class = OtherDriverPaymentListRetrieveSerializer
    filterset_class = OtherDriverPaymentFilter
    ordering_fields = '__all__'
    filename = 'other-driver-payments'
    title = "لیست پرداخت رانندگان متفرقه"

    def get_queryset(self):
        qs = OtherDriverPayment.objects.hasAccess(self.request.method).filter(driving__car__owner=Car.OTHER)
        return self.filterset_class(self.request.GET, queryset=qs).qs

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class LadingBillSeriesListExportView(LadingBillSeriesListView, BaseListExportView):
    filename = 'Lading Bill Series'
    title = "لیست سری های بارنامه"

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class LadingBillNumberListExportView(LadingBillNumberListView, BaseListExportView):
    filename = 'Lading Bill Numbers'
    title = "شماره های بارنامه"

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class RemittanceListExportView(RemittanceListView, BaseListExportView):
    filename = 'Remitances'
    title = "لیست حواله ها"

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class OilCompanyLadingFormExportView(OilCompanyLadingListView, BaseExportView):
    filename = 'other-driver-payment'

    context = {
        'title': 'بارگیری شرکت نفت',
        'verifier_form_name': None
    }

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)


class OilCompanyLadingListExportView(OilCompanyLadingListView, BaseListExportView):
    filename = 'Oil Company Ladings'
    title = "لیست بارگیری های شرکت نفت"

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)


class OilCompanyLadingItemListExportView(OilCompanyLadingItemListView, BaseListExportView):
    filename = 'Oil Company Lading Items'
    title = "لیست بارگیری های شرکت نفت همراه با جزئیات"

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)
