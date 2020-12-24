import json
import re
from io import BytesIO

import pandas
import xlsxwriter
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from wkhtmltopdf.views import PDFTemplateView

from accounts.accounts.models import Account
from factors.models import Factor
from factors.serializers import TransferListRetrieveSerializer, AdjustmentListRetrieveSerializer
from helpers.exports import get_xlsx_response
from helpers.functions import get_object_account_names, rgetattr
from reports.lists.views import SanadListView, FactorListView, TransactionListView, TransferListView, \
    AdjustmentListView, WarehouseHandlingListView
from reports.models import ExportVerifier
from sanads.models import Sanad
from transactions.models import Transaction


class BaseExportView(APIView, PDFTemplateView):
    # filename = 'my_pdf'
    template_name = 'export/form_export.html'

    cmd_options = {
        'margin-top': 3,
        'footer-center': '[page]/[topage]'
    }
    queryset = None
    filterset_class = None
    context = {}
    template_prefix = None

    def get_template_prefix(self):
        if self.template_prefix:
            return self.template_prefix
        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.get_serializer().Meta.model.__name__).lower()

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        print(qs)

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user,
            'print_document': print_document
        }

        template_prefix = self.get_template_prefix()
        context['form_content_template'] = 'export/{}_form_content.html'.format(template_prefix)
        context['right_header_template'] = 'export/{}_right_header.html'.format(template_prefix)

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
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

    def pdf_response(self, request, *args, **kwargs):
        self.filename = "{}.pdf".format(self.filename)
        return super().get(request, user=request.user, *args, **kwargs)

    def print_response(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            context=self.get_context_data(user=request.user, print_document=True)
        )

    def export(self, request, export_type, *args, **kwargs):
        if export_type == 'xlsx':
            return self.xlsx_response(request, *args, **kwargs)
        elif export_type == 'pdf':
            return self.pdf_response(request, *args, **kwargs)
        else:
            return self.print_response(request, *args, **kwargs)


class BaseListExportView(PDFTemplateView):
    """
    Use this class after the list class, then override get method and call `get_response`
    """
    filename = None
    title = None
    context = {}
    filters = []

    template_name = 'export/list_export.html'
    pagination_class = None

    def get_additional_data(self):
        """
        Data to put above the table in text, value format
        :return: array of {text: '...', value: '...'}
        """
        return []

    def get_headers(self):
        headers = self.request.GET.get('headers', "[]")
        headers = json.loads(headers)
        return headers

    def get_header_texts(self):
        headers = self.get_headers()
        return ['#'] + [header['text'] for header in headers]

    def get_header_values(self):
        headers = self.get_headers()
        return [header['value'] for header in headers]

    def get_rows(self):
        return self.filterset_class(self.request.GET, queryset=self.get_queryset()).qs.all()

    def get_filters(self):
        filters = []
        data = self.request.GET.copy()
        data.pop('headers', None)
        data.pop('token', None)
        headers = self.get_headers()
        keys = list(data.keys())
        keys.sort()
        for key in keys:

            text = [header['text'] for header in headers if header['value'].replace('.', '__') in key]
            if len(text):
                text = text[0]
            else:
                continue

            value = data[key]
            if key.endswith('gt') or key.endswith('gte'):
                text = "از {}".format(text)
            elif key.endswith('lt') or key.endswith('lte'):
                text = "تا {}".format(text)
            elif key.endswith('startswith'):
                text = "{} شروع شود با".format(text)
            elif key.endswith('icontains'):
                text = "{} دارا باشد".format(text)

            filters.append({
                'text': text,
                'value': value
            })

        filters = self.filters + filters

        return filters

    def get_context_data(self, user, print_document=False, **kwargs):
        context = {
            'company': user.active_company,
            'user': user,
            'title': self.title,
            'headers': self.get_header_texts(),
            'values': self.get_header_values(),
            'raw_headers': self.get_headers(),
            'rows': self.get_rows(),
            'filters': self.get_filters(),
            'print_document': print_document,
            'additional_data': self.get_additional_data()
        }

        context.update(self.context)

        return context

    def get_response(self, request, *args, **kwargs):
        export_type = kwargs.get('export_type')

        if export_type == 'xlsx':
            return get_xlsx_response('{}.xlsx'.format(self.filename), self.get_xlsx_data(self.get_rows()))
        elif export_type == 'pdf':
            self.filename = "{}.pdf".format(self.filename)
            return super().get(request, user=request.user, *args, **kwargs)
        else:
            return render(
                request,
                'export/list_export.html',
                context=self.get_context_data(user=request.user, print_document=True)
            )

    def get_xlsx_data(self, items):
        data = [
            [self.title],
            *[[data['text'], data['value']] for data in self.get_additional_data()],
            self.get_header_texts()
        ]
        i = 0
        for item in items:
            i += 1
            row = [i]
            for header in self.get_headers():
                row.append(
                    rgetattr(item, header['value'])
                )
            data.append(row)

        return data


class SanadExportView(SanadListView, BaseExportView):
    filename = 'documents'

    context = {
        'title': 'سند حسابداری',
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
        for item in sanad.items.order_by('order').all():
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
    filename = 'factors'
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
            'fpi': {
                'title': 'موجودی اول دوره',
                'verifier_form_name': ExportVerifier.FIRST_PERIOD_INVENTORY
            },
        }

        factorType = self.type
        summarized = request.GET.get('summarized', 'false') == 'true'
        hide_factor = request.GET.get('hide_factor', 'false') == 'true'
        hide_expenses = request.GET.get('hide_expenses', 'false') == 'true'
        hide_remain = request.GET.get('hide_remain', 'false') == 'true'
        hide_prices = request.GET.get('hide_prices', 'false') == 'true'

        if factorType == Factor.CONSUMPTION_WARE:
            hide_expenses = True
            hide_remain = True
            hide_prices = True

        title = names[factorType]['title']

        if not factorType:
            return Response(["No factor type specified"], status=status.HTTP_400_BAD_REQUEST)

        self.context = {
            'title': title,
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
    filename = 'transfers'
    context = {}
    pagination_class = None

    def get_queryset(self):
        return TransferListRetrieveSerializer(
            self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs,
            many=True
        ).data

    def get(self, request, export_type, *args, **kwargs):
        self.context = {
            'title': 'انتقال',
            'verifier_form_name': ExportVerifier.TRANSFER
        }
        return self.export(request, export_type, *args, **kwargs)


class AdjustmentExportView(AdjustmentListView, BaseExportView):
    filename = 'adjustments'
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
            title = 'رسید تعدیل انبار'
        else:
            title = 'حواله تعدیل انبار'

        self.context = {
            'title': title,
            'verifier_form_name': adjustment_type
        }
        return self.export(request, export_type, *args, **kwargs)


class TransactionExportView(TransactionListView, BaseExportView):
    filename = 'transactions'
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
            'title': formName[0][1],
            'verifier_form_name': verifier_form_name
        }
        return self.export(request, export_type, *args, **kwargs)


class WarehouseHandlingExportView(WarehouseHandlingListView, BaseExportView):
    context = {}
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        self.context = {
            'title': 'انبارگردانی',
            'verifier_form_name': 'warehouseHandling',
            'hide_remains': request.GET.get('hide_remains', 'false') == 'true'
        }
        return self.export(request, export_type, *args, **kwargs)


class ImprestSettlementExportView(TransactionListView, BaseExportView):
    filename = 'imprestSettlement'
    template_prefix = 'imprest_settlement'
    pagination_class = None
    context = {
        'title': 'تسویه تنخواه'
    }

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    @staticmethod
    def get_xlsx_data(imprest: Transaction):
        settlement = imprest.imprestSettlement
        data = [
            [
                "شماره: {}".format(settlement.code),
                "تاریخ: {}".format(str(settlement.date)),
                "تنخواه گردان: {}".format(imprest.account.name),
                "شماره پرداخت تنخواه: {}".format(imprest.code),
                "مبلغ تنخواه: {}".format(imprest.sanad.bed),
                "تاریخ: {}".format(str(settlement.date)),
                "توضیحات: {}".format(settlement.explanation)
            ],
            ['ردیف', 'تاریخ', 'شرح تنخواه', 'نام حساب', 'مبلغ']
        ]
        i = 0
        for item in settlement.items.all():
            i += 1
            data.append([
                i,
                item.date,
                item.explanation,
                get_object_account_names(item),
                item.value,
            ])
        data.append(['', '', '', 'جمع', settlement.settled_value])
        data.append(['', '', '', 'اختلاف', imprest.sanad.bed - settlement.settled_value])

        return data
