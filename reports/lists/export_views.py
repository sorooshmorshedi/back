from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateView

from companies.models import Company
from factors.models import Factor
from reports.lists.filters import SanadFilter
from reports.lists.views import SanadListView, FactorListView, TransactionListView
from sanads.sanads.models import Sanad
from sanads.sanads.serializers import SanadSerializer
from sanads.transactions.models import Transaction


class BaseExportView(PDFTemplateView):
    # filename = 'my_pdf.pdf'
    # template_name = 'reports/sanads.html'

    cmd_options = {
        'margin-top': 3,
        'footer-center': '[page]/[topage]'
    }
    queryset = None
    filterset_class = None
    context = {}

    def get_context_data(self, print_document=False, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.first()
        context['forms'] = self.get_queryset()
        context['company'] = company
        context['financial_year'] = company.get_financial_year()
        context['print_document'] = print_document
        context.update(self.context)
        return context

    def export(self, request, export_type, *args, **kwargs):
        self.queryset = self.filterset_class(request.GET, queryset=self.queryset).qs
        pdf = export_type == 'pdf'
        if pdf:
            return super().get(request, *args, **kwargs)
        else:
            return render(request, self.template_name, context=self.get_context_data(print_document=True))


class SanadExportView(SanadListView, BaseExportView):
    filename = 'documents.pdf'
    template_name = 'reports/sanads.html'
    context = {
        'form_name': 'سند حسابداری',
    }
    pagination_class = None
    queryset = Sanad.objects.order_by('code')

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)


class FactorExportView(FactorListView, BaseExportView):
    filename = 'factors.pdf'
    template_name = 'reports/factors.html'
    context = {}
    pagination_class = None

    def get(self, request, export_type, *args, **kwargs):
        formNames = {
            'buy': 'فاکتور خرید',
            'sale': 'فاکتور فروش',
            'backFromBuy': 'فاکتور برگشت از خرید',
            'backFromSale': 'فاکتور برگشت از فروش',
        }
        factorType = request.GET.get('type', None)
        if not factorType:
            return Response(["No factor type specified"], status=status.HTTP_400_BAD_REQUEST)
        self.context = {
            'form_name': formNames[factorType],
            'show_warehouse': factorType != 'sale',
        }
        return self.export(request, export_type, *args, **kwargs)


class TransactionExportView(TransactionListView, BaseExportView):
    filename = 'transactions.pdf'
    template_name = 'reports/transactions.html'
    context = {}
    pagination_class = None

    def get(self, request, export_type, *args, **kwargs):
        transactionType = request.GET.get('type', None)
        if not transactionType:
            return Response(["No transaction type specified"], status=status.HTTP_400_BAD_REQUEST)
        formName = [t for t in Transaction.TYPES if transactionType in t]
        if not formName:
            return Response(["Invalid type"], status=status.HTTP_400_BAD_REQUEST)
        self.context = {
            'form_name': formName[0][1],
        }
        return self.export(request, export_type, *args, **kwargs)

