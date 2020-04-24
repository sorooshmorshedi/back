from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateView
from factors.serializers import TransferListRetrieveSerializer
from reports.lists.views import SanadListView, FactorListView, TransactionListView, TransferListView
from reports.models import ExportVerifier
from transactions.models import Transaction


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

    def get_context_data(self, user, print_document=False, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = self.get_queryset()
        context['company'] = user.active_company
        context['financial_year'] = user.active_financial_year
        context['user'] = user
        context['print_document'] = print_document
        context.update(self.context)
        return context

    def export(self, request, export_type, *args, **kwargs):
        pdf = export_type == 'pdf'
        if pdf:
            return super().get(request, user=request.user, *args, **kwargs)
        else:
            return render(request, self.template_name,
                          context=self.get_context_data(user=request.user, print_document=True))


class SanadExportView(SanadListView, BaseExportView):
    filename = 'documents.pdf'
    template_name = 'reports/sanads.html'
    context = {
        'form_name': 'سند حسابداری',
        'verifier_form_name': ExportVerifier.SANAD
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)


class FactorExportView(FactorListView, BaseExportView):
    filename = 'factors.pdf'
    template_name = 'reports/factors.html'
    context = {}
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        names = {
            'buy': {
                'title': 'فاکتور خرید',
                'verifier_form_name': ExportVerifier.FACTOR_BUY
            },
            'sale': {
                'title':  'فاکتور فروش',
                'verifier_form_name': ExportVerifier.FACTOR_SALE
            },
            'backFromBuy': {
                'title':  'فاکتور برگشت از خرید',
                'verifier_form_name': ExportVerifier.FACTOR_BACK_FROM_BUY
            },
            'backFromSale': {
                'title': 'فاکتور برگشت از فروش',
                'verifier_form_name': ExportVerifier.FACTOR_BACK_FROM_SALE
            }
        }

        factorType = request.GET.get('type', None)
        summarized = request.GET.get('summarized', 'false') == 'true'
        pre_factor = request.GET.get('pre_factor', 'false') == 'true'
        hide_factor = request.GET.get('hide_factor', 'false') == 'true'
        hide_expenses = request.GET.get('hide_expenses', 'false') == 'true'
        hide_remain = request.GET.get('hide_remain', 'false') == 'true'
        hide_prices = request.GET.get('hide_prices', 'false') == 'true'

        pre_factor = True

        form_name = names[factorType]['title']

        if pre_factor:
            form_name = "پیش {}".format(form_name)

        if not factorType:
            return Response(["No factor type specified"], status=status.HTTP_400_BAD_REQUEST)

        self.context = {
            'form_name': form_name,
            'verifier_form_name': names[factorType]['verifier_form_name'],
            'show_warehouse': factorType != 'sale',
            'hide_factor': hide_factor,
            'hide_expenses': hide_expenses,
            'summarized': summarized,
            'hide_remain': hide_remain,
            'hide_prices': hide_prices,
            'pre_factor': pre_factor
        }
        return self.export(request, export_type, *args, **kwargs)


class TransferExportView(TransferListView, BaseExportView):
    filename = 'transfers.pdf'
    template_name = 'reports/transfers.html'
    context = {}
    pagination_class = None

    def get_queryset(self):
        return TransferListRetrieveSerializer(
                self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs,
                many=True
            ).data

    def get(self, request, export_type, *args, **kwargs):
        self.context = {
            'form_name': 'انتقال',
            'verifier_form_name': ExportVerifier.TRANSFER
        }
        return self.export(request, export_type, *args, **kwargs)


class TransactionExportView(TransactionListView, BaseExportView):
    filename = 'transactions.pdf'
    template_name = 'reports/transactions.html'
    context = {}
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        transactionType = request.GET.get('type', None)
        if not transactionType:
            return Response(["No transaction type specified"], status=status.HTTP_400_BAD_REQUEST)

        formName = [t for t in Transaction.TYPES if transactionType in t]
        if transactionType == Transaction.RECEIVE:
            verifier_form_name = ExportVerifier.TRANSACTION_RECEIVE
        else:
            verifier_form_name = ExportVerifier.TRANSACTION_PAYMENT

        if not formName:
            return Response(["Invalid type"], status=status.HTTP_400_BAD_REQUEST)
        self.context = {
            'form_name': formName[0][1],
            'verifier_form_name': verifier_form_name
        }
        return self.export(request, export_type, *args, **kwargs)

