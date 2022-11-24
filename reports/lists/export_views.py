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

from contracting.models import Tender, Contract, Statement, Supplement
from factors.models import Factor
from factors.serializers import TransferListRetrieveSerializer, AdjustmentListRetrieveSerializer
from helpers.exports import get_xlsx_response
from helpers.functions import get_object_account_names, rgetattr
from reports.lists.views import SanadListView, FactorListView, TransactionListView, TransferListView, \
    AdjustmentListView, WarehouseHandlingListView, TenderListView, ContractListView, StatementListView, \
    SupplementListView
from reports.models import ExportVerifier
from sanads.models import Sanad
from transactions.models import Transaction, TransactionItem


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
    right_header_template = None

    template_name = 'export/list_export.html'
    pagination_class = None

    def get_additional_data(self):
        """
        Data to put above the table in text, value format
        :return: array of {text: '...', value: '...'}
        """
        return []

    def get_applied_filters(self):
        applied_filters = self.request.GET.get('applied_filters', "[]")
        applied_filters = json.loads(applied_filters)
        return applied_filters

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

    def get_appended_rows(self):
        return []

    def get_right_header_template(self):
        return self.right_header_template

    def get_filters(self):
        filters = []
        data = self.request.GET.copy()
        data.pop('headers', None)
        data.pop('applied_filters', None)
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
            'appended_rows': self.get_appended_rows(),
            'applied_filters': self.get_applied_filters(),
            'print_document': print_document,
            'additional_data': self.get_additional_data(),
            'right_header_template': self.get_right_header_template(),
            'filters': []
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
        applied_filters = self.get_applied_filters()
        filters_text = ""
        for applied_filter in applied_filters:
            filters_text += applied_filter['text']
            type_text = applied_filter.get('typeText')
            if type_text:
                filters_text += " ({})".format(type_text)
            filters_text += ": {}  -  ".format(applied_filter['value'])

        data = [
            [self.title],
            ["فیلتر های اعمال شده:", filters_text],
            *[[data['text'], data['value']] for data in self.get_additional_data()],
            self.get_header_texts()
        ]
        i = 0
        for item in list(items) + self.get_appended_rows():
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
        if self.request.GET.get('view_list') == 'true':
            self.template_name = 'export/sanad_list.html'

        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        if self.request.GET.get('view_list') == 'true':
            self.template_name = 'export/sanad_list.html'

        return self.export(request, export_type, *args, **kwargs)

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
            i = 0
            if self.request.GET.get('view_list') == 'true':
                data += self.get_xlsx_data(self.get_context_data(user=request.user)['forms'])
            else:
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

    def get_xlsx_data(self, sanads: Sanad):
        if self.request.GET.get('view_list') == 'true':
            data = [
                ['ردیف', 'عطف', 'شماره', 'بدهکار', 'بستانکار', 'تاریخ', 'سیستمی', 'قطعی', 'توضیحات', 'کاربر', ]
            ]
            i = 1
            for sanad in sanads:
                if sanad.is_auto_created == True:
                    auto_create = '✔'
                else:
                    auto_create = '✖'
                if sanad.is_defined == True:
                    defined = '✔'
                else:
                    defined = '✖'

                data.append(
                    [i, sanad.local_id, sanad.code, sanad.bed, sanad.bes, str(sanad.date), auto_create, defined, sanad.explanation, str(self.request.user)]
                )
                i += 1

        else:
            data = [
                [
                    "شماره: {}".format(sanads.code),
                    "تاریخ: {}".format(str(sanads.date)),
                    "توضیحات: {}".format(sanads.explanation)
                ],
                ['ردیف', 'حساب', 'شناور', 'مرکز هزینه و درآمد', 'توضیحات', 'بدهکار', 'بستانکار']
            ]
            i = 0
            for item in sanads.items.order_by('order').all():
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
            data.append(['', '', '', '', 'جمع', sanads.bed, sanads.bes])

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
            'rc': {
                'title': 'رسید',
                'verifier_form_name': ExportVerifier.FACTOR_RECEIPT
            },
            'rm': {
                'title': 'حواله',
                'verifier_form_name': ExportVerifier.FACTOR_REMITTANCE
            },
        }

        factor_type = self.type
        summarized = request.GET.get('summarized', 'false') == 'true'
        hide_factor = request.GET.get('hide_factor', 'false') == 'true'
        hide_expenses = request.GET.get('hide_expenses', 'false') == 'true'
        show_remain = not request.GET.get('hide_remain', 'false') == 'true'
        hide_prices = request.GET.get('hide_prices', 'false') == 'true'
        receipt = request.GET.get('receipt', 'false') == 'true'

        if factor_type == Factor.CONSUMPTION_WARE:
            hide_expenses = True
            show_remain = False
            hide_prices = True

        if receipt:
            if factor_type == Factor.BUY:
                title = "رسید انبار"
            else:
                title = "حواله انبار"
        else:
            title = names[factor_type]['title']
            if self.is_pre_factor:
                title = "پیش {}".format(title)

        if not factor_type:
            return Response(["No factor type specified"], status=status.HTTP_400_BAD_REQUEST)

        self.context = {
            'title': title,
            'verifier_form_name': names[factor_type]['verifier_form_name'],
            'show_warehouse': factor_type != 'sale',
            'hide_factor': hide_factor,
            'hide_expenses': hide_expenses,
            'summarized': summarized,
            'show_remain': show_remain,
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

    def get_xlsx_data(self):
        wareHouseHandling = self.get_queryset().first()
        wares = wareHouseHandling.items.all()
        data = []
        data.append(['انبارگردانی'])
        data.append(
            ['تاریخ آغاز ', wareHouseHandling.start_date, ' ', ' تاریخ شمارش ', wareHouseHandling.counting_date, '',
             'تاریخ ثبت انبارگردانی  ', wareHouseHandling.submit_date])

        data.append(['انبارگردان', self.request.user, ' ', 'انبار', wareHouseHandling.warehouse.name, '',
                     'شرح', wareHouseHandling.explanation])
        data.append([])
        i = 1

        if self.request.GET.get('hide_remains') == 'true':
            data.append(['#', 'کد کالا', 'نام کالا', 'واحد', 'موجودی شمارش شده', 'توضیحات'])
            for item in wares:
                data.append([i, item.ware.code, item.ware.name, item.ware.salePrices.first().unit])
            return data
        else:
            data.append(['#', 'کد کالا', 'نام کالا', 'واحد', 'موجودی شمارش شده', 'مانده سیستم', 'مغایرت', 'توضیحات'])
            for item in wares:
                data.append(
                    [i, item.ware.code, item.ware.name, item.ware.salePrices.first().unit, item.warehouse_remain,
                     item.system_remain, item.contradiction, item.explanation])
                i += 1
            return data

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
            i = 0
            for form in self.get_context_data(user=request.user)['forms']:
                print(form)
                data = self.get_xlsx_data()

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


class TenderExportView(TenderListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'tenders'

    context = {
        'title': 'مناقصه',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
            i = 0
            data += self.get_xlsx_data(self.get_context_data(user=request.user)['forms'])
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

    @staticmethod
    def get_xlsx_data(tender: Tender):
        data = [
            [
                'لیست مناقصه ها'
            ],
            ['کد', 'عنوان', 'توضیحات', 'استان', 'شهر', 'طبقه بندی', 'مناقصه گذار', 'مهلت دریافت اسناد',
             'مهلت ارسال پیشنهاد', 'بازگشایی پاکت', 'اعتبار پیشنهاد']
        ]
        for form in tender:
            data.append([
                form.code,
                form.title,
                form.explanation,
                form.province,
                form.city,
                form.get_classification_display(),
                form.bidder,
                form.received_deadline,
                form.send_offer_deadline,
                form.opening_date,
                form.offer_expiration,
            ])
        return data


class ContractExportview(ContractListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'Contract'

    context = {
        'title': 'قرارداد',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        mySum = 0
        for form in qs:
            mySum += form.amount

        context = {
            'mySum': mySum,
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
            data += self.get_xlsx_data(self.get_context_data(user=request.user)['forms'])
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

    @staticmethod
    def get_xlsx_data(contract: Contract):
        data = [
            [
                'لیست قرارداد ها'
            ],
            ['مناقصه', 'عنوان', 'پیمانکار', 'کد', 'مبلغ', 'از تاریخ', 'تا تاریخ',
             'حداکثر تغییر مبلغ', 'تاریخ ثبت', 'تاریخ شروع', 'حسن انجام کار', 'علی الحساب بیمه', 'سایر']
        ]
        sum = 0
        for form in contract:
            sum += form.amount
            data.append([
                form.tender.title,
                form.title,
                form.contractor,
                form.code,
                form.amount,
                form.from_date,
                form.to_date,
                form.max_change_amount,
                form.registration,
                form.inception,
                form.doing_job_well,
                form.insurance_payment,
                form.other,
            ])
        data.append([' ', ' ', ' ', 'جمع مبالغ قرارداد ها', sum])
        return data


class ContractDetailExportview(ContractListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'ContractDetail'
    template_prefix = 'contractDetail'

    context = {
        'title': 'جزییات کامل قرارداد',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, pk, export_type, *args, **kwargs):
        statement = Statement.objects.filter(contract=pk)
        supplement = Supplement.objects.filter(contract=pk)
        contract = Contract.objects.get(pk=pk)
        receive = contract.received_transaction.all()
        payment = contract.guarantee_document_transaction.all()
        payment_ids = []
        for pay in payment:
            payment_ids.append(pay.id)
        paymentItem = TransactionItem.objects.filter(transaction__in=payment_ids)
        receice_ids = []
        for rec in receive:
            receice_ids.append(rec.id)
        receieveItem = TransactionItem.objects.filter(transaction__in=receice_ids)
        self.context['supplement'] = supplement
        self.context['statement'] = statement
        self.context['receive'] = receive
        self.context['payments'] = payment
        self.context['paymentItem'] = paymentItem
        self.context['receieveItem'] = receieveItem
        return self.export(request, export_type, pk, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        mySum = 0
        for form in qs:
            mySum += form.amount

        context = {
            'mySum': mySum,
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
            data += self.get_xlsx_data(self.get_context_data(user=request.user, context=self.context)['forms'])
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

    @staticmethod
    def get_xlsx_data(contract: Contract, ):
        statements = Statement.objects.filter(contract=contract[0])
        supplements = Supplement.objects.filter(contract=contract[0])
        payment_transaction = Transaction.objects.filter(contract_guarantee=contract[0])
        print(payment_transaction)
        payment_ids = []
        for payment in payment_transaction:
            payment_ids.append(payment.id)
        payment_items = TransactionItem.objects.filter(transaction_id__in=payment_ids)
        receive_transactions = Transaction.objects.filter(contract_received=contract[0])
        receive_ids = []
        for transaction in receive_transactions:
            receive_ids.append(transaction.id)
        receive_items = TransactionItem.objects.filter(transaction_id__in=receive_ids)

        data = [
            [
                ' قرارداد '
            ],
            ['مناقصه', 'عنوان', 'پیمانکار', 'کد', 'مبلغ', 'از تاریخ', 'تا تاریخ',
             'حداکثر تغییر مبلغ', 'تاریخ ثبت', 'تاریخ شروع', 'حسن انجام کار', 'علی الحساب بیمه', 'سایر']
        ]
        for form in contract:
            data.append([
                form.tender.title,
                form.title,
                form.contractor,
                form.code,
                form.amount,
                form.from_date,
                form.to_date,
                form.max_change_amount,
                form.registration,
                form.inception,
                form.doing_job_well,
                form.insurance_payment,
                form.other,
            ])
        data.append([' '])
        data.append([' '])
        data.append(['صورت وضعیت ها'])
        data.append(['کد', 'نوع', 'قرارداد', ' مبلغ', ' مبلغ کارکرد تا صورت وضعیت قبل',
                     ' مبلغ کارکرد تا صورت این صورت وضعیت', 'شماره', 'تاریخ', 'توضیحات'])
        for statement in statements:
            data.append([
                statement.code,
                statement.get_type_display(),
                statement.contract.title,
                statement.value,
                statement.previous_statement_value,
                statement.present_statement_value,
                statement.serial,
                statement.date,
                statement.explanation,
            ])
        data.append([' '])
        data.append([' '])
        data.append(['الحاقیه ها'])
        data.append(['کد', 'قرارداد', 'تاریخ جدید قرارداد', ' مبلغ تغییر', 'تاریخ ثبت الحاقیه ',
                     'توضیحات'])
        for supplement in supplements:
            data.append([
                supplement.code,
                supplement.contract.title,
                supplement.new_contract_date,
                supplement.value,
                supplement.date,
                supplement.explanation,
            ])
        data.append([' '])
        data.append([' '])
        data.append(['اسناد ضمانتی پرداختی'])
        for transaction in payment_transaction:
            data.append(['کد و نام حساب:', 'کد اقتصادی', 'شماره ملی', ' شرح '])
            data.append([
                transaction.account,
                transaction.account.eghtesadi_code,
                transaction.account.melli_code,
                transaction.explanation,
            ])
            data.append(['نوع', 'نام حساب', 'مبلغ', ' شماره پیگیری', 'تاریخ دریافت ',
                         'سررسید', 'نام بانک', 'شرح ردیف'])
            for payment_item in payment_items:
                if payment_item.transaction.id == transaction.id:
                    data.append([
                        payment_item.type,
                        payment_item.type.account,
                        payment_item.value,
                        payment_item.documentNumber,
                        payment_item.date,
                        payment_item.due,
                        payment_item.bankName,
                        payment_item.explanation,
                    ])
            data.append([' '])

        data.append([' '])
        data.append([' '])
        data.append(['دریافت'])
        for transaction in receive_transactions:
            data.append(['کد و نام حساب:', 'کد اقتصادی', 'شماره ملی', ' شرح '])
            data.append([
                transaction.account,
                transaction.account.eghtesadi_code,
                transaction.account.melli_code,
                transaction.explanation,
            ])
            data.append(['نوع', 'نام حساب', 'مبلغ', ' شماره پیگیری', 'تاریخ دریافت ',
                         'سررسید', 'نام بانک', 'شرح ردیف'])
            for receive_item in receive_items:
                if receive_item.transaction.id == transaction.id:
                    data.append([
                        receive_item.type,
                        receive_item.type.account,
                        receive_item.value,
                        receive_item.documentNumber,
                        receive_item.date,
                        receive_item.due,
                        receive_item.bankName,
                        receive_item.explanation,
                    ])
            data.append([' '])

        return data


class StatementExportView(StatementListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'Statement'

    context = {
        'title': 'صورت وضعیت',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        mySum = 0
        for form in qs:
            mySum += form.value

        context = {
            'mySum': mySum,
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
            data += self.get_xlsx_data(self.get_context_data(user=request.user)['forms'])
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

    @staticmethod
    def get_xlsx_data(statement: Statement):
        data = [
            [
                'لیست صورت وضعیت ها'
            ],
            ['کد', 'نوع', 'قرارداد', ' مبلغ', ' مبلغ کارکرد تا صورت وضعیت قبل',
             ' مبلغ کارکرد تا صورت این صورت وضعیت', 'شماره', 'تاریخ', 'توضیحات']
        ]
        sum = 0
        for form in statement:
            sum += form.value
            data.append([
                form.code,
                form.get_type_display(),
                form.contract.title,
                form.value,
                form.previous_statement_value,
                form.present_statement_value,
                form.serial,
                form.date,
                form.explanation,
            ])
        data.append([' ', ' ', 'جمع مبالغ', sum])
        return data


class SupplementExportView(SupplementListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'Supplement'

    context = {
        'title': 'الحاقیه',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        mySum = 0
        for form in qs:
            mySum += form.value

        context = {
            'mySum': mySum,
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
            data += self.get_xlsx_data(self.get_context_data(user=request.user)['forms'])
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

    @staticmethod
    def get_xlsx_data(supplement: Supplement):
        data = [
            [
                'لیست الحاقیه ها'
            ],
            ['کد', 'قرارداد', 'تاریخ جدید قرارداد', ' مبلغ تغییر', 'تاریخ ثبت الحاقیه ',
             'توضیحات']
        ]
        sum = 0
        for form in supplement:
            sum += form.value
            data.append([
                form.code,
                form.contract.title,
                form.new_contract_date,
                form.value,
                form.date,
                form.explanation,
            ])
        data.append([' ', ' ', 'جمع مبالغ', sum])
        return data
