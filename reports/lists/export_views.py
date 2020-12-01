from io import BytesIO

import pandas
import xlsxwriter
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateView

from factors.models import Factor, WarehouseHandling
from factors.serializers import TransferListRetrieveSerializer, AdjustmentListRetrieveSerializer, \
    WarehouseHandlingListRetrieveSerializer
from reports.lists.views import SanadListView, FactorListView, TransactionListView, TransferListView, \
    AdjustmentListView, WarehouseHandlingListView
from reports.models import ExportVerifier
from sanads.models import Sanad
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
        if export_type == 'xlsx':

            sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

            with BytesIO() as b:
                writer = pandas.ExcelWriter(b, engine='xlsxwriter')
                data = []

                bordered_rows = []
                i = 0
                for form in self.get_context_data(user=request.user)['forms']:
                    data += self.get_xlsx_data(form)

                    bordered_rows.append([i, len(data) - 1])

                    i = len(data) + 2

                    data.append([])
                    data.append([])

                df = pandas.DataFrame(data)
                df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False,
                    header=False
                )
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                worksheet.right_to_left()

                border_fmt = workbook.add_format({'bottom': 1, 'top': 1, 'left': 1, 'right': 1})

                for bordered_row in bordered_rows:
                    worksheet.conditional_format(xlsxwriter.utility.xl_range(
                        bordered_row[0], 0, bordered_row[1], len(df.columns) - 1
                    ), {'type': 'no_errors', 'format': border_fmt})
                writer.save()
                response = HttpResponse(b.getvalue(), content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(sheet_name)
                return response

        elif export_type == 'pdf':
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

    @staticmethod
    def get_xlsx_data(sanad: Sanad):
        data = [
            [
                "شماره: {}".format(sanad.code),
                "تاریخ: {}".format(str(sanad.date)),
                "توضیحات: {}".format(sanad.explanation)
            ],
            ['ردیف', 'حساب', 'شناور', 'مرکز هزینه و درآمد', 'توضیحات', 'بدهکار', 'بستانکار']
        ]
        i = 0
        for item in sanad.items.all():
            i += 1
            data.append([
                i,
                item.account.name,
                item.floatAccount.name if item.floatAccount else ' - ',
                item.costCenter.name if item.costCenter else ' - ',
                item.explanation,
                item.bed,
                item.bes,
            ])
        data.append(['', '', '', '', 'جمع', sanad.bed, sanad.bes])

        return data


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
                'title': 'فاکتور فروش',
                'verifier_form_name': ExportVerifier.FACTOR_SALE
            },
            'backFromBuy': {
                'title': 'فاکتور برگشت از خرید',
                'verifier_form_name': ExportVerifier.FACTOR_BACK_FROM_BUY
            },
            'backFromSale': {
                'title': 'فاکتور برگشت از فروش',
                'verifier_form_name': ExportVerifier.FACTOR_BACK_FROM_SALE
            },
            'cw': {
                'title': 'حواله کالای مصرفی',
                'verifier_form_name': ExportVerifier.CONSUMPTION_WARE_REMITTANCE
            },
        }

        factorType = request.GET.get('type', None)
        summarized = request.GET.get('summarized', 'false') == 'true'
        hide_factor = request.GET.get('hide_factor', 'false') == 'true'
        hide_expenses = request.GET.get('hide_expenses', 'false') == 'true'
        hide_remain = request.GET.get('hide_remain', 'false') == 'true'
        hide_prices = request.GET.get('hide_prices', 'false') == 'true'

        if factorType == Factor.CONSUMPTION_WARE:
            hide_expenses = True
            hide_remain = True
            hide_prices = True

        form_name = names[factorType]['title']

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


class AdjustmentExportView(AdjustmentListView, BaseExportView):
    filename = 'adjustments.pdf'
    template_name = 'reports/adjustments.html'
    context = {}
    pagination_class = None

    def get_queryset(self):
        return AdjustmentListRetrieveSerializer(
            self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs,
            many=True
        ).data

    def get(self, request, export_type, *args, **kwargs):
        adjustment_type = request.GET.get('type', None)
        if adjustment_type == 'ia':
            form_name = 'رسید تعدیل انبار'
        else:
            form_name = 'حواله تعدیل انبار'

        self.context = {
            'form_name': form_name,
            'verifier_form_name': adjustment_type
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


class WarehouseHandlingExportView(WarehouseHandlingListView, BaseExportView):
    filename = 'warehouse_handlings.pdf'
    template_name = 'reports/warehouse_handling.html'
    context = {}
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        self.context = {
            'verifier_form_name': 'warehouseHandling',
            'hide_remains': request.GET.get('hide_remains', 'false') == 'true'
        }
        return self.export(request, export_type, *args, **kwargs)
