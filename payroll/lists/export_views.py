import datetime

import jdatetime
import pandas
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse

from numpy import unique

from payroll.lists.views import WorkshopListView, PersonnelListView, PersonnelFamilyListView, ContractRowListView, \
    ContractListView, WorkshopPersonnelListView, LeaveOrAbsenceListView, MissionListView, HRLetterListView, \
    LoanListView, DeductionListView, ListOfPayItemListView, ListOfPayListView, LoanItemListView, \
    ListOfPayInsuranceListView, ListOfPayItemInsuranceListView, PersonTaxListView, TaxListView, WorkshopAbsenceListView, \
    AdjustmentListView, TaxRowListView
from payroll.models import Workshop, Personnel, PersonnelFamily, ContractRow, WorkshopPersonnel, Contract, \
    LeaveOrAbsence, Mission, Loan, OptionalDeduction, HRLetter, LoanItem, ListOfPayItem, ListOfPay, Adjustment
from reports.lists.export_views import BaseExportView, BaseListExportView


class WorkshopExportview(WorkshopListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'Workshop'

    context = {
        'title': 'کارگاه',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
    def get_xlsx_data(workshop: Workshop):
        data = [
            [
                'لیست کارگاه ها'
            ],
            ['کد کارگاه', 'نام کارگاه', 'نام کارفرما', 'آدرس', 'کد پستی',
             'کد شعبه', 'نام شعبه', 'وضعیت', 'نهایی', 'پیشفرض']
        ]
        for form in workshop:
            data.append([
                form.workshop_code,
                form.name,
                form.employer_name,
                form.address,
                form.postal_code,
                form.branch_code,
                form.branch_name,
                form.active_display,
                form.verify_display,
                form.default_display,
            ])
        return data


class PersonnelExportview(PersonnelListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'Personnel'

    context = {
        'title': 'پرسنل',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
    def get_xlsx_data(personnel: Personnel):
        data = [
            [
                'لیست پرسنل'
            ],
            ['نام', 'نام خانوادگی', 'نام پدر', 'کشور', 'ملیت', 'کد پرسنلی', 'جنسبت', 'خدمت سربازی',
             'کد ملی', 'شماره شناسنامه', 'تاریخ تولد', 'تاریخ صدور شناسنامه', 'محل تولد', 'محل صدور شناسنامه',
             'بخش محل صدور', 'وضعیت تاهل', 'تعداد فرزندان', 'پیش شماره', 'تلفن', 'موبایل یک', 'موبایل دو',
             'آدرس', 'کد پستی', 'بیمه تامین اجتماعی', 'شماره بیمه', 'مدرک تحصیلی', 'رشته تحصیلی', 'نوع دانشگاه',
             'نام دانشگاه', 'نام بانک', 'شماره حساب حقوق', 'َشماره شبا', 'وضعیت', 'نهایی']
        ]
        for form in personnel:
            data.append([
                form.name,
                form.last_name,
                form.father_name,
                form.country,
                form.get_nationality_display(),
                form.personnel_code,
                form.get_gender_display(),
                form.get_military_service_display(),
                form.national_code,
                form.identity_code,
                form.date_of_birth,
                form.date_of_exportation,
                form.location_of_birth,
                form.location_of_exportation,
                form.sector_of_exportation,
                form.get_marital_status_display(),
                form.child_number,
                form.city_phone_code,
                form.phone_number,
                form.mobile_number_1,
                form.mobile_number_2,
                form.address,
                form.postal_code,
                form.insurance,
                form.insurance_code,
                form.get_degree_education_display(),
                form.field_of_study,
                form.get_university_type_display(),
                form.university_name,
                form.account_bank_name,
                form.account_bank_number,
                form.sheba_number,
                form.active_display,
                form.verify_display,

            ])
        return data


class PersonnelFamilyExportview(PersonnelFamilyListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'personnel_family'

    context = {
        'title': 'خانواده پرسنل',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
    def get_xlsx_data(personnel_family: PersonnelFamily):
        data = [
            [
                'لیست خانواده پرسنل'
            ],
            ['پرسنل', 'نام', 'نام خانوادگی', 'کد ملی', 'تاریخ تولد', 'نسبت', 'وضعیت تاهل',
             'خدمت سربازی', 'وضعیت تحصیل', 'وضعیت جسمی', 'وضعیت', 'نهایی']
        ]
        for form in personnel_family:
            data.append([
                form.personnel.full_name,
                form.name,
                form.last_name,
                form.national_code,
                form.date_of_birth,
                form.get_relative_display(),
                form.get_marital_status_display(),
                form.get_military_service_display(),
                form.get_study_status_display(),
                form.get_physical_condition_display(),
                form.active_display,
                form.verify_display,

            ])
        return data


class ContractRowExportview(ContractRowListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'contract_row'

    context = {
        'title': 'ردیف پیمان',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
        context['form_content_template'] = 'export/contract_row_content.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(contract_row: ContractRow):
        data = [
            [
                'لیست ردیف پیمان'
            ],
            ['کارگاه', 'ردیف پیمان', 'شماره پیمان', 'تاریخ پیمان', 'تاریخ شروع', 'تاریخ پایان', 'نام واگذار کننده',
             'کد ملی واگذار کننده', 'کد کارگاه واگذار کننده', ' مبلغ اولیه پیمان', ' مبلغ فعلی پیمان',
             'شعبه', 'وضعیت', 'پیشفرض', 'نهایی']
        ]
        for form in contract_row:
            data.append([
                form.workshop.name,
                form.contract_row,
                form.contract_number,
                form.registration_date,
                form.from_date,
                form.now_date,
                form.assignor_name,
                form.assignor_national_code,
                form.assignor_workshop_code,
                form.round_amount_with_comma,
                form.round_now_amount_with_comma,
                form.branch,
                form.status_display,
                form.default_display,
                form.verify_display

            ])
        return data


class WorkshopPersonnelExportView(WorkshopPersonnelListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'workshop_personnel'

    context = {
        'title': 'پرسنل در کارگاه',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
    def get_xlsx_data(workshop_personnel: WorkshopPersonnel):
        data = [
            [
                'لیست  پرسنل در کارگاه ها'
            ],
            ['کارگاه', 'پرسنل', 'تاریخ استخدام', 'عنوان شغلی',
             'سابقه بیمه قبلی خارچ از کارگاه', 'سابقه بیمه قبلی در این کارگاه', 'سابقه سابقه بیمه جاری در این کارگاه',
             'مجموع سوابق بیمه ای', 'سمت', 'رسته شغلی', 'محل خدمت', ' وضعیت محل خدمت', 'نوع استخدام',
             'نوع قرارداد', 'وضعیت کارمند', 'نهایی']
        ]
        for form in workshop_personnel:
            data.append([
                form.workshop.workshop_title,
                form.personnel.full_name,
                form.employment_date,
                form.title.name + ' ' + form.title.code,
                form.previous_insurance_history_out_workshop,
                form.previous_insurance_history_in_workshop,
                form.current_insurance,
                form.insurance_history_total,
                form.job_position,
                form.get_job_group_display(),
                form.job_location,
                form.get_job_location_status_display(),
                form.get_employment_type_display(),
                form.get_contract_type_display(),
                form.get_employee_status_display(),
                form.verify_display,
            ])
        return data


class ContractExportView(ContractListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'contract'

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

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user,
            'print_document': print_document
        }

        template_prefix = self.get_template_prefix()
        context['form_content_template'] = 'export/{}_form_content.html'.format(template_prefix)
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
            ['پرسنل در کارگاه', 'تاریخ شروع قرارداد', 'تاریخ پایان قرارداد', 'تاریخ ترک کار',
             'بیمه میشود؟', 'شماره بیمه', 'تاریخ اضافه شدن به لیست بیمه', 'نهایی']
        ]
        for form in contract:
            data.append([
                form.workshop_personnel.my_title,
                form.contract_from_date,
                form.contract_to_date,
                form.quit_job_date,
                form.is_insurance_display,
                form.insurance_number,
                form.insurance_add_date,
                form.verify_display,
            ])
        return data


class LeaveOrAbsenceExportView(LeaveOrAbsenceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'absence'

    context = {
        'title': 'مرخصی و غیبت',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
    def get_xlsx_data(absence: LeaveOrAbsence):
        data = [
            [
                'لیست مرخصی و غیبت ها'
            ],
            ['پرسنل در کارگاه', 'نوع مرخصی', 'نوع  ', 'نوع  ', 'از تاربخ',
             'تا تاربخ ', ' تاربخ ', 'از ساعت', 'تا ساعت', 'علت مرخصی', 'توضیحات', 'نهایی']
        ]
        for form in absence:
            data.append([
                form.workshop_personnel.my_title,
                form.get_leave_type_display(),
                form.get_entitlement_leave_type_display(),
                form.get_matter73_leave_type_display(),
                form.from_date,
                form.to_date,
                form.date,
                form.from_hour,
                form.to_hour,
                form.cause_of_incident,
                form.explanation,
                form.verify_display,
            ])
        return data


class AbsenceRequestExportView(LeaveOrAbsenceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'absence_request'

    context = {
        'title': 'فرم مرخصی',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
        context['form_content_template'] = 'export/absence_request_form.html'
        context['right_header_template'] = 'export/absence_request_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(absence: LeaveOrAbsence):
        data = [
            [
                'لیست مرخصی و غیبت ها'
            ],
            ['پرسنل در کارگاه', 'نوع مرخصی', 'نوع  ', 'نوع  ', 'از تاربخ',
             'تا تاربخ ', 'از ساعت', 'تا ساعت', 'علت مرخصی', 'توضیحات']
        ]
        for form in absence:
            data.append([
                form.workshop_personnel.my_title,
                form.get_leave_type_display(),
                form.get_entitlement_leave_type_display(),
                form.get_matter73_leave_type_display(),
                form.from_date,
                form.to_date,
                form.from_hour,
                form.to_hour,
                form.cause_of_incident,
                form.explanation
            ])
        return data


class MissionExportView(MissionListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'mission'

    context = {
        'title': 'ماموریت',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        template_prefix = self.get_template_prefix()
        context['form_content_template'] = 'export/{}_form_content.html'.format(template_prefix)
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(mission: Mission):
        data = [
            [
                'لیست ماموریت ها'
            ],
            ['پرسنل در کارگاه', 'نوع ماموریت', 'موضوع', 'از تاربخ',
             'تا تاربخ ', 'از ساعت', 'تا ساعت', 'تاربخ', 'مکان', 'توضیحات', 'نهایی']
        ]
        for form in mission:
            data.append([
                form.workshop_personnel.my_title,
                form.get_mission_type_display(),
                form.topic,
                form.from_date,
                form.to_date,
                form.from_hour,
                form.to_hour,
                form.date,
                form.location,
                form.explanation,
                form.verify_display
            ])
        return data


class MissionRequestExportView(MissionListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'mission_request'

    context = {
        'title': 'فرم ماموریت',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user,
            'print_document': print_document
        }

        context['form_content_template'] = 'export/mission_request_form.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    @staticmethod
    def get_xlsx_data(mission: Mission):
        data = [
            [
                'لیست ماموریت ها'
            ],
            ['پرسنل در کارگاه', 'نوع ماموریت', 'موضوع', 'از تاربخ',
             'تا تاربخ ', 'از ساعت', 'تا ساعت', 'تاربخ', 'مکان', 'توضیحات']
        ]
        data.append([
            mission.workshop_personnel.my_title,
            mission.get_mission_type_display(),
            mission.topic,
            mission.from_date,
            mission.to_date,
            mission.from_hour,
            mission.to_hour,
            mission.date,
            mission.location,
            mission.explanation
        ])
        return data


class ContractFormExportView(ContractListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'contract_form'

    context = {
        'title': 'قرارداد کار مدت معین',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user,
            'print_document': print_document
        }

        context['form_content_template'] = 'export/contract_form.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
            ['پرسنل در کارگاه', 'تاریخ شروع قرارداد', 'تاریخ پایان قرارداد', 'تاریخ ترک کار', 'نهایی']
        ]
        for form in contract:
            data.append([
                form.workshop_personnel.my_title,
                form.contract_from_date,
                form.contract_to_date,
                form.quit_job_date,
                form.verify_display
            ])
        return data


class HRLetterExportView(HRLetterListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'hr_letter'

    context = {
        'title': 'حکم کارگزینی',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.name,
            'print_document': print_document
        }

        context['form_content_template'] = 'export/hr_letter_form.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(hr: HRLetter):
        data = [
            [
                'لیست حکم های کارگزینی'
            ],
            [''],
        ]
        for form in hr:
            if form.is_template == 't':
                data.append([
                    'قالب',
                    form.name,
                ])
            else:
                data.append([
                    form.contract_info['personnel_name'] + 'در کارگاه ' + form.contract_info['workshop_name'],
                ])

            data.append([
                'عنوان',
                'مبلغ',
            ])
            data.append([
                'حداقل مزد روزانه',
                form.hoghooghe_roozane_amount,
            ])
            data.append([
                'پایه سنوات روزانه',
                form.paye_sanavat_amount,
            ])
            data.append([
                'حق مسکن',
                form.haghe_maskan_amount,
            ])
            data.append([
                'حق بن خار و بار',
                form.bon_kharo_bar_amount,
            ])
            data.append([
                'حق سرپرستی',
                form.haghe_sarparasti_amount,
            ])
            data.append([
                'حق مدیریت',
                form.haghe_modiriyat_amount,
            ])
            data.append([
                'حق جذب',
                form.haghe_jazb_amount,
            ])
            data.append([
                'فوق العاده شغل',
                form.fogholade_shoghl_amount,
            ])
            data.append([
                'حق تحصیلات',
                form.haghe_tahsilat_amount,
            ])
            data.append([
                'فوق العاده سختی کار',
                form.fogholade_sakhti_kar_amount,
            ])
            data.append([
                'حق آنکال',
                form.haghe_ankal_amount,
            ])
            data.append([
                'فوق العاده بدی هوا',
                form.fogholade_badi_abohava_amount,
            ])
            data.append([
                'محرومیت از تسحیلات',
                form.mahroomiat_tashilat_zendegi_amount,
            ])
            data.append([
                'فوق العاده محل خدمت',
                form.fogholade_mahal_khedmat_amount,
            ])
            data.append([
                'فوق العاده محیط کار',
                form.fogholade_sharayet_mohit_kar_amount,
            ])
            data.append([
                'ایاب و ذهاب',
                form.ayabo_zahab_amount,
            ])
            data.append([
                'یارانه غذا',
                form.yarane_ghaza_amount,
            ])
            data.append([
                'حق شیر',
                form.haghe_shir_amount,
            ])
            data.append([
                'حق تاهل',
                form.haghe_taahol_amount,
            ])
            data.append([
                'کمک هزینه مهدکودک',
                form.komakhazine_mahdekoodak_amount,
            ])
            data.append([
                'کمک هزینه ورزش',
                form.komakhazine_varzesh_amount,
            ])
            data.append([
                'کمک هزینه موبایل',
                form.komakhazine_mobile_amount,
            ])
            data.append([
                'مزایای مستمر غیرنقدی',
                form.mazaya_mostamar_gheyre_naghdi_amount,
            ])
            data.append([
                'نهایی',
                form.verify_display,
            ])
        return data


class LoanExportView(LoanListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'loan'

    context = {
        'title': 'وام یا مساعده',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        template_prefix = self.get_template_prefix()
        context['form_content_template'] = 'export/{}_form_content.html'.format(template_prefix)
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(loan: Loan):
        data = [
            [
                'لیست وام یا مساعده ها'
            ],
            ['پرسنل در کارگاه', 'نوع', 'مبلغ', 'تعداد قسط',
             'مبلغ قسط', ' تاربخ پرداخت', 'تاربخ سررسید', ' اقساط پرداخت شده', 'تصفیه شد', 'نهایی']
        ]
        for form in loan:
            data.append([
                form.workshop_personnel.my_title,
                form.get_loan_type_display(),
                form.amount,
                form.episode,
                form.get_pay_episode,
                form.pay_date,
                form.end_date,
                form.episode_payed,
                form.pay_done,
                form.verify_display,
            ])
        return data


class LoanRequestExportView(LoanListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'loan_request'

    context = {
        'title': ' در خواست وام یا مساعده',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/loan_request_form.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(loan: Loan):
        data = [
            [
                'لیست وام یا مساعده ها'
            ],
            ['پرسنل در کارگاه', 'نوع', 'مبلغ', 'تعداد قسط',
             'مبلغ قسط', ' تاربخ پرداخت', 'تاربخ سررسید', ' اقساط پرداخت شده', 'تصفیه شد']
        ]
        for form in loan:
            data.append([
                form.workshop_personnel.my_title,
                form.get_loan_type_display(),
                form.amount,
                form.episode,
                form.get_pay_episode,
                form.pay_date,
                form.end_date,
                form.episode_payed,
                form.pay_done,
            ])
        return data


class DeductionExportView(DeductionListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'deduction'

    context = {
        'title': 'کسورات اختیاری',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        template_prefix = self.get_template_prefix()
        context['form_content_template'] = 'export/{}_form_content.html'.format(template_prefix)
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(deduction: OptionalDeduction):
        data = [
            [
                'لیست کسورات اختیاری'
            ],
            ['پرسنل در کارگاه', 'نوع', 'نام قالب', 'عنوان', 'مبلغ', 'تعداد قسظ',
             'مبلغ قسظ', ' تاربخ پرداخت', ' اقساط پرداخت شده', 'تصفیه شد', 'نهایی']
        ]
        for form in deduction:
            data.append([
                form.workshop_personnel,
                form.is_template_display,
                form.template_name,
                form.name,
                form.round_amount_with_comma,
                form.episode,
                form.round_pay_episode_with_comma,
                form.start_date,
                form.episode_payed,
                form.pay_done,
                form.verify_display,
            ])
        return data


class LoanRequestExportView(LoanListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'loan_request'
    context = {
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        if qs.first().loan_type == 'd':
            context = {
                'title': 'فرم درخواست مساعده',
                'forms': qs,
                'company': user.active_company,
                'financial_year': user.active_financial_year,
                'user': user.get_full_name(),
                'print_document': print_document
            }
        else:
            context = {
                'title': 'فرم درخواست وام',
                'forms': qs,
                'company': user.active_company,
                'financial_year': user.active_financial_year,
                'user': user.get_full_name(),
                'print_document': print_document
            }

        context['form_content_template'] = 'export/loan_request_form.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(loan: Loan):
        data = [
            [
                'لیست وام یا مساعده ها'
            ],
            ['پرسنل در کارگاه', 'نوع', 'مبلغ', 'تعداد قسط',
             'مبلغ قسط', ' تاربخ پرداخت', 'تاربخ سررسید', ' اقساط پرداخت شده', 'تصفیه شد', 'نهایی']
        ]
        for form in loan:
            data.append([
                form.workshop_personnel.my_title,
                form.get_loan_type_display(),
                form.amount,
                form.episode,
                form.get_pay_episode,
                form.pay_date,
                form.end_date,
                form.episode_payed,
                form.pay_done,
                form.verify_display,
            ])
        return data


class PayslipExportView(ListOfPayItemListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'payslip'

    context = {
        'title': 'فیش حقوق',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/payslip_form.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay_item: ListOfPayItem):
        data = [
            [
                'فیش حقوق'
            ],
        ]
        for form in list_of_pay_item:
            data.append([
                'کد پرسنلی',
                form.workshop_personnel.personnel.personnel_code,
                'نام و نام خانوادگی',
                form.workshop_personnel.personnel.full_name,
                'شماره حساب',
                form.workshop_personnel.personnel.bank_cart_number,
            ])
            data.append([
                'کارکرد',
                '',
                'اضافات(ريال)',
                '',
                'کسورات(ريال)',
                '',
            ])
            data.append([
                'کارکرد عادی(روز)',
                form.normal_worktime,
                'حقوق پایه',
                form.hoghoogh_mahane,
                'بیمه تامین اجتماعی',
                form.haghe_bime_bime_shavande,
            ])
            data.append([
                'کارکرد اضافه کاری (ساعت)',
                form.ezafe_kari,
                'مبلغ اضافه کاری',
                form.ezafe_kari_total,
                'مالیات',
                form.total_tax,
            ])
            data.append([
                'تعطیل کاری (ساعت)',
                form.tatil_kari,
                'مبلغ تعطیل کاری',
                form.tatil_kari_total,
                'سایر بدهی ها',
                0,
            ])
            data.append([
                'کسر کار (ساعت)',
                form.kasre_kar,
                'حق مسکن',
                form.haghe_maskan,
                'مبلغ کسر کار',
                form.kasre_kar_total,
            ])
            data.append([
                'غیبت',
                form.absence_day,
                'حق خارو بار (بن کارگری)',
                form.kharo_bar,
                'سایر کسورات',
                form.sayer_kosoorat,
            ])
            data.append([
                'کارکرد واقعی',
                form.real_worktime,
                'حق جذب',
                form.haghe_jazb,
                'مساعده یا وام',
                form.check_and_get_loan_episode,
            ])
            data.append([
                'جمع مرخصی استحقاقی',
                form.entitlement_leave_day,
                'پایه سنوات',
                form.sanavat_mahane,
                'کسورات اختیاری',
                form.check_and_get_optional_deduction_episode,
            ])
            data.append([
                'جمع مرخصی استعلاجی',
                form.illness_leave_day,
                'حق سنوات',
                form.haghe_sanavat_total,
                '',
                '',
            ])
            data.append([
                'روز ماموریت',
                form.mission_sum,
                'مبلغ ماموریت',
                form.mission_total,
                '',
                '',
            ])
            if form.shab_kari_total != 0:
                data.append([
                    'شب کاری(روز)',
                    form.shab_kari,
                    'مبلغ شب کاری',
                    form.shab_kari_total,
                    '',
                    '',
                ])
            if form.aele_mandi != 0:
                data.append([
                    'تعداد اولاد مشمول',
                    form.aele_mandi_child,
                    'حق اولاد',
                    form.aele_mandi,
                    '',
                    '',
                ])
            if form.nobat_kari_sob_shab_total != 0:
                data.append([
                    ' نوبت کاری صبح و شب(روز)',
                    form.nobat_kari_sob_shab,
                    'مبلغ نوبت کاری صبح و شب',
                    form.nobat_kari_sob_shab_total,
                    '',
                    '',
                ])
            if form.nobat_kari_sob_asr_total != 0:
                data.append([
                    ' نوبت کاری صبح و عصر(روز)',
                    form.nobat_kari_sob_asr,
                    'مبلغ نوبت کاری صبح و عصر',
                    form.nobat_kari_sob_asr_total,
                    '',
                    '',
                ])
            if form.nobat_kari_asr_shab_total != 0:
                data.append([
                    ' نوبت کاری عصر و شب(روز)',
                    form.nobat_kari_asr_shab,
                    'مبلغ نوبت کاری عصر و شب',
                    form.nobat_kari_asr_shab_total,
                    '',
                    '',
                ])
            if form.nobat_kari_sob_asr_shab_total != 0:
                data.append([
                    ' نوبت کاری صبح، عصر و شب(روز)',
                    form.nobat_kari_sob_asr_shab,
                    'مبلغ نوبت کاری صبح، عصر و شب',
                    form.nobat_kari_sob_asr_shab_total,
                    '',
                    '',
                ])
            if form.padash_total != 0:
                data.append([
                    '',
                    '',
                    'عیدی یا پاداش',
                    form.padash_total,
                    '',
                    '',
                ])
            if form.haghe_sarparasti != 0:
                data.append([
                    '',
                    '',
                    'حق سرپرستی',
                    form.haghe_sarparasti,
                    '',
                    '',
                ])
            if form.haghe_modiriyat != 0:
                data.append([
                    '',
                    '',
                    'حق مدیریت',
                    form.haghe_modiriyat,
                    '',
                    '',
                ])
            if form.fogholade_shoghl != 0:
                data.append([
                    '',
                    '',
                    'فوق العاده شفل',
                    form.fogholade_shoghl,
                    '',
                    '',
                ])
            if form.haghe_tahsilat != 0:
                data.append([
                    '',
                    '',
                    'حق تحصیلات',
                    form.haghe_tahsilat,
                    '',
                    '',
                ])
            if form.fogholade_sakhti_kar != 0:
                data.append([
                    '',
                    '',
                    'فوق العاده سختی کار',
                    form.fogholade_sakhti_kar,
                    '',
                    '',
                ])
            if form.haghe_ankal != 0:
                data.append([
                    '',
                    '',
                    'حق آنکال',
                    form.haghe_ankal,
                    '',
                    '',
                ])
            if form.fogholade_badi != 0:
                data.append([
                    '',
                    '',
                    'فوق العاده بدی آب و هوا',
                    form.fogholade_badi,
                    '',
                    '',
                ])
            if form.mahroomiat_tashilat_zendegi != 0:
                data.append([
                    '',
                    '',
                    'فوق العاده محرومیت از تسهیلات زندگی',
                    form.mahroomiat_tashilat_zendegi,
                    '',
                    '',
                ])
            if form.fogholade_mahal_khedmat != 0:
                data.append([
                    '',
                    '',
                    'فوق العاده محل خدمت',
                    form.fogholade_mahal_khedmat,
                    '',
                    '',
                ])
            if form.fogholade_sharayet_mohit_kar != 0:
                data.append([
                    '',
                    '',
                    'فوق العاده محیط کار',
                    form.fogholade_sharayet_mohit_kar,
                    '',
                    '',
                ])
            if form.ayabo_zahab != 0:
                data.append([
                    '',
                    '',
                    'ایاب و ذهاب',
                    form.ayabo_zahab,
                    '',
                    '',
                ])
            if form.yarane_ghaza != 0:
                data.append([
                    '',
                    '',
                    'یارانه غذا',
                    form.yarane_ghaza,
                    '',
                    '',
                ])
            if form.haghe_shir != 0:
                data.append([
                    '',
                    '',
                    'حق شیر',
                    form.haghe_shir,
                    '',
                    '',
                ])
            if form.haghe_taahol != 0:
                data.append([
                    '',
                    '',
                    'حق تاهل',
                    form.haghe_taahol,
                    '',
                    '',
                ])
            if form.komakhazine_mahdekoodak != 0:
                data.append([
                    '',
                    '',
                    'کمک هزینه مهدکودک',
                    form.komakhazine_mahdekoodak,
                    '',
                    '',
                ])
            if form.komakhazine_varzesh != 0:
                data.append([
                    '',
                    '',
                    'کمک هزینه ورزش',
                    form.komakhazine_varzesh,
                    '',
                    '',
                ])
            if form.komakhazine_mobile != 0:
                data.append([
                    '',
                    '',
                    'کمک هزینه موبایل',
                    form.komakhazine_mobile,
                    '',
                    '',
                ])
            if form.mazaya_mostamar_gheyre_naghdi != 0:
                data.append([
                    '',
                    '',
                    'مزایای مستمر غیر نقدی',
                    form.mazaya_mostamar_gheyre_naghdi,
                    '',
                    '',
                ])
            if form.mazaya_gheyr_mostamar != 0:
                data.append([
                    '',
                    '',
                    'مزایای غیر مستمر غیر نقدی',
                    form.mazaya_gheyr_mostamar,
                    '',
                    '',
                ])
            if form.sayer_ezafat != 0:
                data.append([
                    '',
                    '',
                    'سایر اضافات',
                    form.sayer_ezafat,
                    '',
                    '',
                ])
        return data


class BankReportExportView(ListOfPayListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'bank_report'

    context = {
        'title': 'خروجی بانک جهت پرداخت حقوق',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/bank_report.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay: ListOfPay):
        data = [
            [
                'خروجی بانک جهت پرداخت حقوق '
            ],
            ['نام و نام خانوادگی', 'مبلغ پرداختی', 'شماره کارت', 'شماره حساب', 'شماره شبا']
        ]
        for forms in list_of_pay:
            for form in forms.bank_report:
                if form['paid'] != 0:
                    data.append([
                        form['name'],
                        form['paid'],
                        form['card'],
                        form['account'],
                        form['sheba'],
                    ])
        return data


class PayFormExportView(ListOfPayListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'pay_form'

    context = {
        'title': 'فرم پرداخت حقوق',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/pay_form.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay: ListOfPay):
        data = [
            [
                'فرم پرداخت حقوق '
            ],
            ['نام و نام خانوادگی', 'حقوق معوقه', 'حقوق قابل پرداخت ماه جاری', 'جمع حقوق قابل پرداخت تا ماه',
             'مبلغ پرداختی', 'حقوق پرداخت نشده']
        ]
        for forms in list_of_pay:
            for form in forms.form_bank_report:
                data.append([
                    form['name'],
                    form['previous'],
                    form['payable'],
                    form['total'],
                    form['paid'],
                    form['unpaid'],
                ])
            data.append([
                'جمع',
                forms.total_un_paid_of_year,
                forms.total_payable,
                forms.total_un_paid,
                forms.total_paid,
                forms.un_paid,
            ])

        return data


class PayrollExportView(ListOfPayListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'payroll_form'

    context = {
        'title': 'حقوق و دستمزد جامع',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/payroll_form.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay: ListOfPay):
        counter = 1
        data = [
            [
                'حقوق و دستمزد جامع '
            ],
            ['ردیف', 'نام و نام خانوادگی', 'تاریخ شروع به کار', 'تاریخ تسوبه', 'عنوان شغل', 'بیمه میشود؟',
             'سابقه بیمه در کارگاه',
             'ردیف پیمان', 'کارکرد عادی', 'مرخصی استحقاقی', '', '', 'مرخصی استعلاجی', 'مرخصی ماده 73',
             'مرخصی بدون حقوق', 'غیبت',
             'کارکرد واقعی', 'حداقل مزد روزانه', 'حقوق پایه ماهانه', 'پایه سنوات روزانه', 'پایه سنوات ماهانه',
             'اضافه کاری', '', 'تعطیل کاری', '', 'شب کاری', '',
             'کسر کار', '', 'ماموریت', '', 'حق خاروبار', 'حق مسکن', 'حق اولاد', '', 'حق جذب', 'پورسانت', 'سایر اضافات',
             'حقوق مزایای کل ماهانه', 'بــیـمـه', '', '', '',
             'حق بیمه سهم بیمه شده', 'معافیت مالیاتی حقوق', 'حقوق مشمول مالیات', 'مالیات حقوق', 'بدهی متفرقه', '', '',
             'حقوق و دستمزد پرداختنی', 'حق بیمه سهم کارفرما', 'بیمه بیکاری'],

            ['', '', '', '', '', '', '', '', '', 'ساعتی', 'روزانه', 'جمع', '', '', '', '',
             '', '', '', '', '', 'ساعت', 'مبلغ', 'ساعت', 'مبلغ', 'ساعت', 'مبلغ',
             'ساعت', 'مبلغ', 'روز', 'مبلغ', '', '', 'تعداد اولاد', 'مبلغ', '', '', '', '', 'دستمزد ماهانه',
             'مزایای ماهانه مشمول مستمر و غیر مستمر',
             'جمع دستمزد مزایای ماهانه مشمول', 'جمع کل دستمزد و مزایای ماهانه',
             '', '', '', '', 'مساعده', 'وام', 'غیره', '   ', '', '']
        ]
        for form in list_of_pay.first().get_items:
            data.append(
                [counter, form.workshop_personnel.personnel.full_name, form.contract.contract_from_date,
                 '', form.workshop_personnel.title.name, form.contract.insurance,
                 form.workshop_personnel.current_insurance,
                 '', form.normal_worktime, form.hourly_entitlement_leave_day, form.daily_entitlement_leave_day,
                 form.entitlement_leave_day, form.illness_leave_day, form.matter_47_leave_day,
                 form.without_salary_leave_day,
                 form.absence_day, form.real_worktime, form.hoghoogh_roozane, form.hoghoogh_mahane, form.sanavat_base,
                 form.sanavat_mahane,
                 form.ezafe_kari, form.ezafe_kari_total, form.tatil_kari, form.tatil_kari_total, form.shab_kari,
                 form.shab_kari_total,
                 form.kasre_kar, form.kasre_kar_total, form.mission_day, form.mission_total,
                 form.get_payslip['additions']['kharo_bar'],
                 form.get_payslip['additions']['hagh_maskan'], form.aele_mandi_child, form.aele_mandi,
                 form.get_payslip['additions']['hagh_jazb'], '',
                 form.sayer_ezafat, form.total_payment, form.data_for_insurance['DSW_MAH'],
                 form.data_for_insurance['DSW_MAZ'],
                 form.data_for_insurance['DSW_MASH'], form.data_for_insurance['DSW_TOTL'],
                 form.data_for_insurance['DSW_BIME'],
                 form.moaf_sum, form.tax_included_payment, form.calculate_month_tax, form.check_and_get_dept_episode,
                 form.check_and_get_loan_episode, form.check_and_get_optional_deduction_episode, form.payable,
                 form.employer_insurance, form.un_employer_insurance]

            )
            counter += 1
        item = list_of_pay.first()
        item = item.total
        data.append(
            ['جمع', '', '', '', '', '', '',
             '', item['normal_worktime'], '', '',
             '', '', '',
             '',
             '', item['real_worktime'], '', item['hoghoogh_mahane'], '',
             item['sanavat_mahane'],
             '', item['ezafe_kari_total'], '', item['tatil_kari_total'], '',
             item['shab_kari_total'],
             '', item['kharo_bar'], '', item['mission_total'],
             item['kharo_bar'],
             item['haghe_maskan'], '', item['aele_mandi'],
             item['haghe_jazb'], '',
             item['sayer_ezafat'], item['total_payment'], '',
             '',
             '', '',
             item['haghe_bime_bime_shavande'],
             '', '', item['total_tax'], item['dept_amount'],
             item['loan_amount'], item['check_and_get_optional_deduction_episode'], item['payable'],
             '', '']

        )

        return data


class LoanItemExportView(LoanItemListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'loan_item'

    context = {
        'title': 'جدول وام',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        template_prefix = self.get_template_prefix()
        context['form_content_template'] = 'export/{}_form_content.html'.format(template_prefix)
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(loan: Loan):
        data = [
            [
                'جدول وام یا مساعده '
            ],
            ['ماه', 'مبلغ هر قسط', 'کارمزد', 'مبلغ قابل پرداخت ماهانه',
             'مبلغ پرداخت شده', ' اضافه/کسر پرداخت ماه جاری', 'مانده تجمیعی وام']
        ]
        for form in loan:
            data.append([
                form.month_display,
                form.amount,
                '',
                form.amount,
                form.payed_amount,
                form.bed_or_bes,
                form.cumulative_balance,
            ])
        return data


class WorkshopInsuranceReportExportView(ListOfPayInsuranceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'workshop_insurance_report'

    context = {
        'title': 'گزارش بیمه',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/insurance_report_form_content.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay: ListOfPay):
        data = [
            [
                'گزارش بیمه '
            ],
        ]
        for form in list_of_pay:
            data.append([
                'کد کارگاه',
                form.data_for_insurance['DSK_ID'],
            ])
            data.append([
                'نام کارگاه',
                form.data_for_insurance['DSK_NAME'],
            ])
            data.append([
                'نام کارفرما',
                form.data_for_insurance['DSK_FARM'],
            ])
            data.append([
                'آدرس کارگاه',
                form.data_for_insurance['DSK_ADRS'],
            ])
            data.append([
                'سال عملکرد',
                form.data_for_insurance['DSK_YY'],
            ])
            data.append([
                'ماه عملکرد',
                form.data_for_insurance['DSK_MM'],
            ])
            data.append([
                'شماره لیست',
                form.data_for_insurance['DSK_LISTNO'],
            ])
            data.append([
                'شرح لیست',
                form.data_for_insurance['DSK_DISC'],
            ])
            data.append([
                'تعداد کارکنان',
                form.data_for_insurance['DSK_NUM'],
            ])
            data.append([
                'مجموع روز های کارکرد',
                form.data_for_insurance['DSK_TDD'],
            ])
            data.append([
                'مجموع دستمزد روزانه',
                form.data_for_insurance['DSK_TROOZ'],
            ])
            data.append([
                'مجموع دستمزد ماهانه',
                form.data_for_insurance['DSK_TMAH'],
            ])
            data.append([
                'مجموع مزایای ماهانه مشمول',
                form.data_for_insurance['DSK_TMAZ'],
            ])
            data.append([
                'مجموع دستمزد و مزایای ماهانه مشمول',
                form.data_for_insurance['DSK_TMASH'],
            ])
            data.append([
                'مجموع دستمزد و مزایای ماهانه مشمول',
                form.data_for_insurance['DSK_TMASH'],
            ])
            data.append([
                'مجموع کل دستمزد و مزایای ماهانه',
                form.data_for_insurance['DSK_TTOTL'],
            ])
            data.append([
                'مجموع حق بیمه سهم بیمه شده',
                form.data_for_insurance['DSK_TBIME'],
            ])
            data.append([
                'مجموع حق بیمه سهم کارفرما',
                form.data_for_insurance['DSK_TKOSO'],
            ])
            data.append([
                'مجموع حق بیمه بیکاری',
                form.data_for_insurance['DSK_TBIC'],
            ])
            data.append([
                'نرخ حق بیمه',
                form.data_for_insurance['DSK_RATE'],
            ])
            data.append([
                'نرخ پورسانتاژ',
                form.data_for_insurance['DSK_PRATE'],
            ])
            data.append([
                'نرخ مشاغل زیان آور',
                form.data_for_insurance['DSK_BIMH'],
            ])
            data.append([
                'ردیف پیمان',
                form.data_for_insurance['DSK_PYM'],
            ])

        return data


class ContractRowInsuranceReportExportView(ListOfPayInsuranceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'contract_row_insurance_report'

    context = {
        'title': 'گزارش بیمه',
    }
    pagination_class = None

    def __init__(self):
        self.contract_row = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, pk,  *args, **kwargs):
        self.contract_row = pk
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        datas = qs.first().data_for_insurance_row(self.contract_row)
        context = {
            'datas': datas,
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/row_insurance_report_form_content.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
            data += self.get_xlsx_data(self.get_context_data(user=request.user)['datas'])
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
    def get_xlsx_data(list_of_pay: ListOfPay):
        data = [
            [
                'گزارش بیمه '
            ],
        ]
        form = list_of_pay
        data.append([
            'کد کارگاه',
            form['DSK_ID'],
        ])
        data.append([
            'نام کارگاه',
            form['DSK_NAME'],
        ])
        data.append([
            'نام کارفرما',
            form['DSK_FARM'],
        ])
        data.append([
            'آدرس کارگاه',
            form['DSK_ADRS'],
        ])
        data.append([
            'سال عملکرد',
            form['DSK_YY'],
        ])
        data.append([
            'ماه عملکرد',
            form['DSK_MM'],
        ])
        data.append([
            'شماره لیست',
            form['DSK_LISTNO'],
        ])
        data.append([
            'شرح لیست',
            form['DSK_DISC'],
        ])
        data.append([
            'تعداد کارکنان',
            form['DSK_NUM'],
        ])
        data.append([
            'مجموع روز های کارکرد',
            form['DSK_TDD'],
        ])
        data.append([
            'مجموع دستمزد روزانه',
            form['DSK_TROOZ'],
        ])
        data.append([
            'مجموع دستمزد ماهانه',
            form['DSK_TMAH'],
        ])
        data.append([
            'مجموع مزایای ماهانه مشمول',
            form['DSK_TMAZ'],
        ])
        data.append([
            'مجموع دستمزد و مزایای ماهانه مشمول',
            form['DSK_TMASH'],
        ])
        data.append([
            'مجموع دستمزد و مزایای ماهانه مشمول',
            form['DSK_TMASH'],
        ])
        data.append([
            'مجموع کل دستمزد و مزایای ماهانه',
            form['DSK_TTOTL'],
        ])
        data.append([
            'مجموع حق بیمه سهم بیمه شده',
            form['DSK_TBIME'],
        ])
        data.append([
            'مجموع حق بیمه سهم کارفرما',
            form['DSK_TKOSO'],
        ])
        data.append([
            'مجموع حق بیمه بیکاری',
            form['DSK_TBIC'],
        ])
        data.append([
            'نرخ حق بیمه',
            form['DSK_RATE'],
        ])
        data.append([
            'نرخ پورسانتاژ',
            form['DSK_PRATE'],
        ])
        data.append([
            'نرخ مشاغل زیان آور',
            form['DSK_BIMH'],
        ])
        data.append([
            'ردیف پیمان',
            form['DSK_PYM'],
        ])

        return data


class PersonInsuranceReportExportView(ListOfPayItemInsuranceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'insurance_report'

    context = {
        'title': 'گزارش بیمه',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/person_insurance_report_form_content.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay_item: ListOfPayItem):
        data = [
            [
                'گزارش بیمه'
            ],
        ]
        for form in list_of_pay_item:
            data.append([
                'کد کارگاه',
                form.data_for_insurance['DSW_ID'],
            ])
            data.append([
                'سال عملکرد',
                form.data_for_insurance['DSW_YY'],
            ])
            data.append([
                'ماه عملکرد',
                form.data_for_insurance['DSW_MM'],
            ])
            data.append([
                'شماره لیست',
                form.data_for_insurance['DSW_LISTNO'],
            ])
            data.append([
                'شماره بیمه',
                form.data_for_insurance['DSW_ID1'],
            ])
            data.append([
                'نام ',
                form.data_for_insurance['DSW_FNAME'],
            ])
            data.append([
                'نام خانوادگی',
                form.data_for_insurance['DSW_LNAME'],
            ])
            data.append([
                'نام پدر',
                form.data_for_insurance['DSW_DNAME'],
            ])
            data.append([
                'شماره شناسنامه',
                form.data_for_insurance['DSW_IDNO'],
            ])
            data.append([
                'محل صدور',
                form.data_for_insurance['DSW_IDPLC'],
            ])
            data.append([
                'تاریخ صدور',
                form.data_for_insurance['DSW_IDATE'],
            ])
            data.append([
                'تاریخ تولد',
                form.data_for_insurance['DSW_BDATE'],
            ])
            data.append([
                'جنسیت',
                form.data_for_insurance['DSW_SEX'],
            ])
            data.append([
                'ملیت',
                form.data_for_insurance['DSW_NAT'],
            ])
            data.append([
                'شرح شغل',
                form.data_for_insurance['DSW_OCP'],
            ])
            data.append([
                'شرح شغل',
                form.data_for_insurance['DSW_OCP'],
            ])
            data.append([
                'تاریخ شروع به کار',
                form.data_for_insurance['DSW_SDATE'],
            ])
            data.append([
                'تاریخ ترک کار',
                form.data_for_insurance['DSW_EDATE'],
            ])
            data.append([
                'تعداد روز های کارکرد',
                form.data_for_insurance['DSW_DD'],
            ])
            data.append([
                'دستمزد روزانه',
                form.data_for_insurance['DSW_ROOZ'],
            ])
            data.append([
                'دستمزد ماهانه',
                form.data_for_insurance['DSW_MAH'],
            ])
            data.append([
                'مزایای ماهانه',
                form.data_for_insurance['DSW_MAZ'],
            ])
            data.append([
                'مجموع دستمزد و مزایای مشمول',
                form.data_for_insurance['DSW_MASH'],
            ])
            data.append([
                'مجموع کل دستمزد و مزایای ماهانه',
                form.data_for_insurance['DSW_TOTL'],
            ])
            data.append([
                'حق بیمه سهم بیمه شده',
                form.data_for_insurance['DSW_BIME'],
            ])
            data.append([
                'نرخ پورسانتاژ',
                form.data_for_insurance['DSW_PRATE'],
            ])
            data.append([
                'کد شغل',
                form.data_for_insurance['DSW_JOB'],
            ])
            data.append([
                'کد ملی',
                form.data_for_insurance['PER_NATCOD'],
            ])
        return data


class PersonTaxReportExportView(PersonTaxListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'person_tax_report'

    context = {
        'title': 'گزارش مالیات',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/person_tax_report.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay_item: ListOfPayItem):
        data = [
            [
                'گزارش مالیات'
            ],
        ]
        for form in list_of_pay_item:
            data.append([
                'کد ملی/کد فراگیر',
                form.workshop_personnel.personnel.national_code,
            ])
            data.append([
                'نوع پرداخت',
                1,
            ])
            data.append([
                'تعداد ماههای کارکرد واقعی از ابتدای سال جاری',
                form.year_real_work_month,
            ])
            data.append([
                'یا این ماه آخرین ماه فعالیت کاریحقوق بگیر میباشد؟',
                0,
            ])
            data.append([
                'نوع ارز',
                85,
            ])
            data.append([
                'نرخ تسعیر ارز',
                1,
            ])
            data.append([
                'تاریخ شروع به کار',
                form.workshop_personnel.employment_date,
            ])
            data.append([
                'تاریخ پایان کار',
                '',
            ])
            data.append([
                'وضعیت کارمند',
                form.workshop_personnel.employee_status,
            ])
            data.append([
                'وضعیت محل خدمت',
                form.workshop_personnel.job_location_status,
            ])
            data.append([
                'ناخالص حقوق و دستمزد مستمر نقدی ماه جاری-ریالی',
                form.tax_naghdi_pension,
            ])
            data.append([
                'پرداختهای مستمر معوق که مالیاتی برای آنها محاسبه نشده است',
                0,
            ])
            data.append([
                'مسکن',
                1,
            ])
            data.append([
                'مبلغ کسر شده از حقوق کارمند بابت مسکن ماه جاری',
                0,
            ])
            data.append([
                'وسیله نقلیه',
                1,
            ])
            data.append([
                'مبلغ کسر شده از حقوق کارمند بابت وسیله نقلیه ماه جاری',
                0,
            ])
            data.append([
                'وسیله نقلیه',
                1,
            ])
            data.append([
                'پرداخت مزایای مستمر غیر نقدی ماه جاری',
                form.gheyre_naghdi_tax_pension,
            ])
            data.append([
                'هزینه های درمانی موضوع ماده 37 ق.م.م.',
                form.hazine_made_137,
            ])
            data.append([
                'سایر حق بیمه پرداختی موضوع ماده 37 ق.م.م.',
                form.kosoorat_insurance,
            ])
            data.append([
                'حق بیمه پرداختی موضوع ماده 37 ق.م.م.',
                form.haghe_bime_moafiat,
            ])
            data.append([
                'تسهیلات اعتباری مسکن از بانکها',
                0,
            ])
            data.append([
                'سایر معافیتها',
                form.total_sayer_moafiat,
            ])
            data.append([
                'ناخالص اضافه کاری ماه جاری',
                form.ezafe_kari_nakhales,
            ])
            data.append([
                'سایر پرداختهای غیر مستمر نقدی ماه جاری',
                form.tax_naghdi_un_pension,
            ])
            data.append([
                'حق ماموریت',
                form.mission_total,
            ])
            data.append([
                'پاداش های مورد یماه جاری',
                0,
            ])
            data.append([
                'پرداختهای غیر مستمر نقدی معوقه ماه جاری',
                0,
            ])
            data.append([
                'کسر میشود:معافیت های غیر مستمر نقدی(شامل بند6ماده91)',
                form.mission_total,
            ])
            data.append([
                'پرداخت مزایای غیر مستمر غیر نقدی ماه جاری',
                form.mazaya_gheyr_mostamar,
            ])
            data.append([
                'عیدی و مزایای پایان سال',
                form.get_padash,
            ])
            data.append([
                'بازخرید مرخصی و بازخرید سنوات-ریالی',
                form.get_hagh_sanavat_and_save_leaves,
            ])
            data.append([
                'کسر میشود:معافیت(فقط برای بند5ماده91)',
                form.get_hagh_sanavat_and_save_leaves,
            ])
            data.append([
                'معافیت مربوط به مناطق آزاد تجاری',
                form.manategh_tejari_moafiat,
            ])
            data.append([
                'معافیت موضوع قانون اجتناب از اخذ مالیات مضاعف',
                form.ejtenab_maliat_mozaaf,
            ])
            data.append([
                'مالیات متعلّقه حقوق و دستمزد مستمر نقدی، درآمدها و مزایای غیر نقدی، پرداختهای غیر مستمر نقدی وغیر نقدی، عیدی و مزایا، بازخرید مرخصی و سنوات ماه جاری',
                form.calculate_month_tax,
            ])
        return data


class TaxReportExportView(TaxListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'tax_report'

    context = {
        'title': 'گزارش مالیات',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/workshop_tax_report.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)
        print(qs)

        return context


class MonthTaxReportExportView(TaxListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'month_tax_report'

    context = {
        'title': ' گزارش خلاصه مالیات',
    }
    pagination_class = None

    def __init__(self):
        self.list_of_pay = []

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        self.list_of_pay.append(ListOfPay.objects.get(id=request.query_params.get('id')))

        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': self.list_of_pay,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/tax_summary_report.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay: ListOfPay):
        data = [
            [
                ' گزارش  خلاصه مالیات '
            ],
        ]
        for form in list_of_pay:
            data.append([
                'سال',
                form.year,
            ])
            data.append([
                'ماه',
                form.month,
            ])
            data.append([
                'بدهی مالیاتی ماه جاری',
                form.month_tax,
            ])
            data.append([
                'بدهی مالیاتی ماه گذشته',
                0,
            ])
            data.append([
                'تاریخ ثبت در دفتر روزنامه',
                form.sign_date,
            ])
            data.append([
                'نحوه پرداخت',
                6,
            ])
            data.append([
                'شماره سریال چک',
                '',
            ])
            data.append([
                'تاریخ چک',
                '',
            ])
            data.append([
                'کد نام بانک',
                '',
            ])
            data.append([
                'نام شعبه',
                '',
            ])
            data.append([
                'شماره حساب',
                '',
            ])
            data.append([
                'مبلغ پرداختی/مبلغ چک',
                '',
            ])
            data.append([
                'تاریخ پرداخت خزانه',
                '',
            ])
            data.append([
                'مبلغ پرداختی خزانه',
                '',
            ])

        return data


class AbsenceReportExportView(WorkshopAbsenceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'absence_report'
    month = []
    year = None

    def __init__(self):
        self.month = []

    context = {
        'title': ' گزارش جامع مرخصی',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, year, month, *args, **kwargs):
        months = month
        self.year = year
        while len(months) > 0:
            self.month.append(int(months[:2]))
            print(self.month)
            new_months = ""
            for i in range(len(months)):
                if i != 0 and i != 1:
                    new_months = new_months + months[i]

            months = new_months
        self.month = unique(self.month)
        return self.export(request, 'html', *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        qs = qs.first()
        form = qs.absence_report(self.year, self.month)
        form['col_number'] = len(form['months']) * 5
        print(form)
        self.month = []
        print(form['col_number'])

        context = {
            'forms': form,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/leave_report_table.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context


class SaveLeaveReportExportView(WorkshopAbsenceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'absence_report'
    month = []
    year = None

    def __init__(self):
        self.month = []

    context = {
        'title': ' گزارش جامع ذخیره مزایای مرخصی',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, year, month, *args, **kwargs):
        months = month
        self.year = year
        while len(months) > 0:
            self.month.append(int(months[:2]))
            print(self.month)
            new_months = ""
            for i in range(len(months)):
                if i != 0 and i != 1:
                    new_months = new_months + months[i]

            months = new_months
        self.month = unique(self.month)
        return self.export(request, 'html', *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        qs = qs.first()
        form = qs.save_leave_report(self.year, self.month)
        form['col_number'] = len(form['months'])
        self.month = []

        context = {
            'forms': form,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/save_leave_report.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context


class EydiReportExportView(WorkshopAbsenceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'eydi_report'
    month = []
    year = None

    def __init__(self):
        self.month = []

    context = {
        'title': ' گزارش جامع عیدی و پاداش',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, year, month, *args, **kwargs):
        months = month
        self.year = year
        while len(months) > 0:
            self.month.append(int(months[:2]))
            new_months = ""
            for i in range(len(months)):
                if i != 0 and i != 1:
                    new_months = new_months + months[i]

            months = new_months
        self.month = unique(self.month)
        return self.export(request, 'html', *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        qs = qs.first()
        form = qs.eydi_report(self.year, self.month)
        form['col_number'] = len(form['months'])
        self.month = []

        context = {
            'forms': form,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/eydi_report.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context


class SanavatReportExportView(WorkshopAbsenceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'haghe_sanavat_report'
    month = []
    year = None

    def __init__(self):
        self.month = []

    context = {
        'title': ' گزارش جامع حق سنوات',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, year, month, *args, **kwargs):
        months = month
        self.year = year
        while len(months) > 0:
            self.month.append(int(months[:2]))
            new_months = ""
            for i in range(len(months)):
                if i != 0 and i != 1:
                    new_months = new_months + months[i]

            months = new_months
        self.month = unique(self.month)
        return self.export(request, 'html', *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        qs = qs.first()
        form = qs.hagh_sanavat_report(self.year, self.month)
        form['col_number'] = len(form['months'])
        self.month = []

        context = {
            'forms': form,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/sanavat_report.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context


class NewPersonTaxReportExportView(WorkshopPersonnelListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'month_tax_report'

    context = {
        'title': 'اطلاعات حقوق بگیر',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/personnel_report_tax.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pay_item: ListOfPayItem):
        data = [
            [
                '  اطلاعات حقوق بگیر (مالیات)'
            ],
        ]
        for form in list_of_pay_item:
            data.append([
                'کد ملی/کد فراگیر',
                form.personnel.national_code,
            ])
            data.append([
                'نام',
                form.personnel.name,
            ])
            data.append([
                'نام خانوادگی',
                form.personnel.last_name,
            ])
            data.append([
                'کشور',
                form.personnel.country,
            ])
            data.append([
                'شناسه کارمند',
                form.personnel.personnel_code,
            ])
            data.append([
                'مدرک تحصیلی',
                form.personnel.degree_education,
            ])
            data.append([
                'سمت',
                form.work_title,
            ])
            data.append([
                'نوع بیمه',
                form.personnel.insurance_for_tax,
            ])
            data.append([
                'نام بیمه',
                '',
            ])
            data.append([
                'شماره بیمه',
                form.personnel.insurance_code,
            ])
            data.append([
                'کد پستی محل سکونت',
                form.personnel.postal_code,
            ])
            data.append([
                'نشانی محل سکونت',
                form.personnel.address,
            ])
            data.append([
                'نوع استخدام',
                form.employment_type,
            ])
            data.append([
                'محل خدمت',
                form.job_location,
            ])
            data.append([
                'وضعیت محل خدمت',
                form.job_location_status,
            ])
            data.append([
                'نوع قرارداد',
                form.contract_type,
            ])
            data.append([
                'پایان کار',
                '',
            ])
            data.append([
                'وضعیت کارمند',
                form.employee_status,
            ])
            data.append([
                'شماره تلفن همراه',
                form.personnel.mobile_number_1,
            ])
            data.append([
                'پست الکترونیک',
                '',
            ])

        return data


class SettlementExportView(WorkshopPersonnelListView, BaseExportView):
    personnel = None
    template_name = 'export/sample_form_export.html'
    filename = 'settlement'
    context = {
        'title': ' تسویه حساب',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, personnel, export_type, *args, **kwargs):
        self.personnel = WorkshopPersonnel.objects.get(id=personnel)
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.personnel
        context = {
            'now': jdatetime.date.today(),
            'form': qs,
            'settlement': qs.settlement,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }
        context['form_content_template'] = 'export/settlement_form.html'
        context['right_header_template'] = 'export/sample_head.html'
        context.update(self.context)
        return context


class AccountBalanceReportExportView(WorkshopPersonnelListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'account_balance'

    context = {
        'title': 'گردش پرداختی حقوق بگیر',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()

        context = {
            'form': qs.first().payment_balance,
            'forms': qs.first(),
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/balance.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context


class AdjustmentExportView(AdjustmentListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'adjustment'

    context = {
        'title': 'تعدیل',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        contract_row = qs.first().contract_row
        context = {
            'contract_row': contract_row,
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/adjustment_content.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(adjustment: Adjustment):
        data = [
            [
                'تعدیل'
            ],
            ['ردیف پیمان', 'تاریخ ثبت تعدیل', 'تاریخ پایان جدید',
             'مبلغ تعدیل قرارداد', 'نوع تعدیل مبلغ', 'توضیحات']
        ]
        for form in adjustment:
            data.append([
                form.contract_row.title,
                form.date,
                form.change_date,
                form.amount_with_comma,
                form.status_display,
                form.explanation,
            ])
        return data


class TaxExportView(TaxRowListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'contract'

    context = {
        'title': 'جدول معافیت مالیاتی',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        items = []
        for item in qs.all():
            items.append(item.tax_row.all())
        context = {
            'forms': qs,
            'items': items,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user,
            'print_document': print_document
        }

        template_prefix = self.get_template_prefix()
        context['form_content_template'] = 'export/tax_row_content.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context


class InsuranceCardexExportview(ListOfPayInsuranceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'InsuranceCardex'

    context = {
        'title': 'کاردکس بیمه',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
        context['form_content_template'] = 'export/insurance_cardex.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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
    def get_xlsx_data(list_of_pays: ListOfPay):
        for list_of_pay in list_of_pays:
            data = [
                [
                    'کاردکس بیمه'
                ],

                [
                    'شماره کارگاه',
                    list_of_pay.workshop.workshop_code,
                    'نام کارفرما',
                    list_of_pay.workshop.employer_name,
                    'نشانی کارگاه',
                    list_of_pay.workshop.address,
                ],
                ['ردیف', 'شماره بیمه', 'نام و نام خانوادگی', 'شغل', 'کد ملی',
                 'کارکرد', 'دستمزد روزانه', 'دستمزد ماهانه', 'مزایای ماهانه',
                 'مجموع دستمزد و مزایای مشمول', 'مجموع کل دستمزد و مزایای ماهانه', 'حق بیمه سهم بیمه شده']
            ]
            counter = 1
            for item in list_of_pay.list_of_pay_item.all():
                if item.is_month_insurance:
                    data.append([
                        counter,
                        item.workshop_personnel.personnel.insurance_code,
                        item.workshop_personnel.personnel.full_name,
                        item.workshop_personnel.title.name,
                        item.workshop_personnel.personnel.identity_code,
                        item.insurance_worktime,
                        item.data_for_insurance['DSW_ROOZ'],
                        item.data_for_insurance['DSW_MAH'],
                        item.data_for_insurance['DSW_MAZ'],
                        item.data_for_insurance['DSW_MASH'],
                        item.data_for_insurance['DSW_TOTL'],
                        item.data_for_insurance['DSW_BIME'],
                    ])
                    counter += 1
            form = list_of_pay
            data.append([
                '', '', '', '', 'جمع',
                form.data_for_insurance['DSK_TDD'],
                form.data_for_insurance['DSK_TROOZ'],
                form.data_for_insurance['DSK_TMAH'],
                form.data_for_insurance['DSK_TMAZ'],
                form.data_for_insurance['DSK_TMASH'],
                form.data_for_insurance['DSK_TTOTL'],
                form.data_for_insurance['DSK_TBIME'],
            ])
            data.append([
                'حق بیمه سهم کارفرما',
                form.data_for_insurance['DSK_TKOSO'],
                'جمع بیمه بیکاری',
                form.data_for_insurance['DSK_TBIC'],
                'جمع  حق بیمه کارگر',
                form.data_for_insurance['DSK_TBIME'],
                'جمع کل حق بیمه پرداختنی',
                form.data_for_insurance['insurance_total'],
            ])
        return data


class RowInsuranceCardexExportview(ListOfPayInsuranceListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'InsuranceCardex'

    context = {
        'title': 'کاردکس بیمه',
    }
    pagination_class = None

    def __init__(self):
        self.contract_row = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, pk,  *args, **kwargs):
        self.contract_row = pk
        return self.export(request, export_type, *args, **kwargs)

    def get_context_data(self, user, print_document=False, **kwargs):
        qs = self.get_queryset()
        datas = qs.first().data_for_insurance_row(self.contract_row)
        items = qs.first().row_list(self.contract_row)
        context = {
            'items': items,
            'datas': datas,
            'forms': qs,
            'company': user.active_company,
            'financial_year': user.active_financial_year,
            'user': user.get_full_name(),
            'print_document': print_document
        }

        context['form_content_template'] = 'export/row_cardex.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
            data += self.get_xlsx_data(self.get_context_data(user=request.user)['datas'])
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

    def get_xlsx_data(self, list_of_pays: ListOfPay):
        list_of_pay = list_of_pays
        data = [
            [
                'کاردکس بیمه'
            ],
            [
                'شماره کارگاه',
                list_of_pay['workshop'].workshop_code,
                'نام کارفرما',
                list_of_pay['workshop'].employer_name,
                'نشانی کارگاه',
                list_of_pay['workshop'].address,
            ],
            ['ردیف', 'شماره بیمه', 'نام و نام خانوادگی', 'شغل', 'کد ملی',
             'کارکرد', 'دستمزد روزانه', 'دستمزد ماهانه', 'مزایای ماهانه',
             'مجموع دستمزد و مزایای مشمول', 'مجموع کل دستمزد و مزایای ماهانه', 'حق بیمه سهم بیمه شده']
        ]
        counter = 1
        for item in list_of_pay['list_of_pays']:
            if item.is_month_insurance:
                data.append([
                    counter,
                    item.workshop_personnel.personnel.insurance_code,
                    item.workshop_personnel.personnel.full_name,
                    item.workshop_personnel.title.name,
                    item.workshop_personnel.personnel.identity_code,
                    item.insurance_worktime,
                    item.data_for_insurance['DSW_ROOZ'],
                    item.data_for_insurance['DSW_MAH'],
                    item.data_for_insurance['DSW_MAZ'],
                    item.data_for_insurance['DSW_MASH'],
                    item.data_for_insurance['DSW_TOTL'],
                    item.data_for_insurance['DSW_BIME'],
                ])
                counter += 1
        form = list_of_pay
        data.append([
            '', '', '', '', 'جمع',
            form['DSK_TDD'],
            form['DSK_TROOZ'],
            form['DSK_TMAH'],
            form['DSK_TMAZ'],
            form['DSK_TMASH'],
            form['DSK_TTOTL'],
            form['DSK_TBIME'],
        ])
        data.append([
            'حق بیمه سهم کارفرما',
            form['DSK_TKOSO'],
            'جمع بیمه بیکاری',
            form['DSK_TBIC'],
            'جمع  حق بیمه کارگر',
            form['DSK_TBIME'],
            'جمع کل حق بیمه پرداختنی',
            form['insurance_total'],
        ])
        return data


class TaxCardexExportView(ListOfPayListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'Workshop'

    context = {
        'title': 'گزارش مالیات ماه',
    }
    pagination_class = None

    def get_queryset(self):
        return self.filterset_class(self.request.GET, queryset=super().get_queryset()).qs

    def get(self, request, export_type, *args, **kwargs):
        return self.export(request, export_type, *args, **kwargs)

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
        context['form_content_template'] = 'export/tax_cardex.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context

    def xlsx_response(self, request, *args, **kwargs):
        sheet_name = '{}.xlsx'.format("".join(self.filename.split('.')[:-1]))

        with BytesIO() as b:
            writer = pandas.ExcelWriter(b, engine='xlsxwriter')
            data = []

            bordered_rows = []
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


    def get_xlsx_data(self, list_of_pays: ListOfPay):
        list_of_pay = list_of_pays.first()
        data = [
            [
                'گزارش مالیات'
            ],
            [
                'تاریخ ثبت در دفتر روزنامه',
                list_of_pay.sign_date,
                'نوع پرداخت',
                1,
                'نوع ارز',
                85,
                'نرخ تسعیر',
                1,

            ],
            ['ردیف', 'کد ملی/کد فراگیر', 'نام و نام خانوادگی', 'تعداد ماههای کارکرد واقعی از ابتدای سال جاری', 'تاریخ شروع به کار',
             'وضعیت کارمند', 'وضعیت محل خدمت', 'ناخالص حقوق و دستمزد مستمر نقدی ماه جاری-ریالی', 'پرداخت مزایای مستمر غیر نقدی ماه جاری',
             'هزینه های درمانی موضوع ماده 37 ق.م.م.', 'حق بیمه پرداختی موضوع ماده 37 ق.م.م.', 'سایر معافیتها', 'ناخالص اضافه کاری ماه جاری',
             'سایر پرداختهای غیر مستمر نقدی ماه جاری', 'کسر میشود:معافیت های غیر مستمر نقدی(شامل بند6ماده91)',
             'پرداخت مزایای غیر مستمر غیر نقدی ماه جاری', 'عیدی و مزایای پایان سال', 'بازخرید مرخصی و بازخرید سنوات-ریالی',
             'کسر میشود:معافیت(فقط برای بند5ماده91)', 'معافیت مربوط به مناطق آزاد تجاری', 'معافیت موضوع قانون اجتناب از اخذ مالیات مضاعف',
             'مالیات متعلّقه حقوق و دستمزد']
        ]

        counter = 1
        for item in list_of_pay.list_of_pay_item.all():
            if item.is_month_tax:
                data.append([
                    counter,
                    item.workshop_personnel.personnel.national_code,
                    item.workshop_personnel.personnel.full_name,
                    item.year_real_work_month,
                    item.contract.tax_add_date,
                    item.workshop_personnel.employee_status,
                    item.workshop_personnel.job_location_status,
                    item.tax_naghdi_pension,
                    item.gheyre_naghdi_tax_pension,
                    item.hazine_made_137,
                    item.haghe_bime_moafiat,
                    item.total_sayer_moafiat,
                    item.ezafe_kari_nakhales,
                    item.tax_naghdi_un_pension,
                    item.mission_total,
                    item.mazaya_gheyr_mostamar,
                    item.padash_total,
                    item.get_hagh_sanavat_and_save_leaves,
                    item.get_hagh_sanavat_and_save_leaves,
                    item.manategh_tejari_moafiat,
                    item.ejtenab_maliat_mozaaf,
                    item.total_tax,
                ])
                counter += 1
        data.append([
            '', '', '', '',  '', '',  'جمع',
            list_of_pay.total_tax_naghdi_pension,
            list_of_pay.total_gheyre_naghdi_tax_pension,
            list_of_pay.total_hazine_made_137,
            list_of_pay.total_haghe_bime_moafiat,
            list_of_pay.total_sayer_moafiat,
            list_of_pay.total_ezafe_kari_nakhales,
            list_of_pay.total_tax_naghdi_un_pension,
            list_of_pay.mission_total,
            list_of_pay.total_mazaya_gheyr_mostamar,
            list_of_pay.padash_total,
            list_of_pay.total_hagh_sanavat_and_save_leaves,
            list_of_pay.total_hagh_sanavat_and_save_leaves,
            list_of_pay.total_manategh_tejari_moafiat,
            list_of_pay.total_ejtenab_maliat_mozaaf,
            list_of_pay.month_tax,
        ])
        return data
