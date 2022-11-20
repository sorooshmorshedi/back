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
    ListOfPayInsuranceListView, ListOfPayItemInsuranceListView, PersonTaxListView, TaxListView, WorkshopAbsenceListView
from payroll.models import Workshop, Personnel, PersonnelFamily, ContractRow, WorkshopPersonnel, Contract, \
    LeaveOrAbsence, Mission, Loan, OptionalDeduction, HRLetter, LoanItem
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
             'کد شعبه', 'نام شعبه']
        ]
        for form in workshop:
            data.append([
                form.code,
                form.name,
                form.employer_name,
                form.address,
                form.postal_code,
                form.branch_code,
                form.branch_name,
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
             'نام دانشگاه', 'نام بانک', 'شماره حساب حقوق', 'َشماره شبا']
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
                form.number_of_childes,
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
             'خدمت سربازی', 'وضعیت تحصیل', 'وضعیت جسمی']
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
    def get_xlsx_data(contract_row: ContractRow):
        data = [
            [
                'لیست ردیف پیمان'
            ],
            ['کارگاه', 'ردیف پیمان', 'شماره پیمان', 'تاریخ پیمان', 'تاریخ شروع', 'تاریخ پایان', 'نام واگذار کننده',
             'کد ملی واگذار کننده', 'کد انبار واگذار کننده', 'حداقل مبلغ پیمان', 'شعبه']
        ]
        for form in contract_row:
            data.append([
                form.workshop.name,
                form.contract_row,
                form.contract_number,
                form.registration_date,
                form.from_date,
                form.to_date,
                form.assignor_name,
                form.assignor_national_code,
                form.assignor_workshop_code,
                form.contract_initial_amount,
                form.branch

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
            ['کارگاه', 'پرسنل',  'تاریخ استخدام', 'عنوان شغلی',
             'سابقه بیمه قبلی خارچ از کارگاه', 'سابقه بیمه قبلی در این کارگاه', 'سابقه سابقه بیمه جاری در این کارگاه',
             'مجموع سوابق بیمه ای', 'سمت', 'رسته شغلی', 'محل خدمت', ' وضعییت محل خدمت', 'نوع استخدام',
             'نوع قرارداد', 'وضعییت کارمند']
        ]
        for form in workshop_personnel:
            data.append([
                form.workshop.workshop_title,
                form.personnel.full_name,
                form.employment_date,
                form.work_title,
                form.previous_insurance_history_out_workshop,
                form.previous_insurance_history_in_workshop,
                form.current_insurance_history_in_workshop,
                form.insurance_history_totality,
                form.job_position,
                form.get_job_group_display(),
                form.job_location,
                form.get_job_location_status_display(),
                form.get_employment_type_display(),
                form.get_contract_type_display(),
                form.get_employee_status_display(),
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
            ['پرسنل در کارگاه', 'تاریخ شروع قرارداد', 'تاریخ پایان قرارداد', 'تاریخ ترک کار']
        ]
        for form in contract:
            data.append([
                form.workshop_personnel.my_title,
                form.contract_from_date,
                form.contract_to_date,
                form.quit_job_date
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
             'تا تاربخ ', 'از ساعت', 'تا ساعت', 'تاربخ', 'مکان', 'توضیحات']
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
                form.explanation
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
                '',
                '',
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
            ['پرسنل در کارگاه', 'قالب است ؟', 'نام قالب', 'عنوان', 'مبلغ', 'تعداد قسظ',
             'مبلغ قسظ', ' تاربخ پرداخت', ' اقساط پرداخت شده', 'تصفیه شد']
        ]
        for form in deduction:
            data.append([
                form.workshop_personnel,
                form.is_template,
                form.template_name,
                form.name,
                form.amount,
                form.episode,
                form.get_pay_episode,
                form.start_date,
                form.episode_payed,
                form.pay_done,
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

        return context


class MonthTaxReportExportView(TaxListView, BaseExportView):
    template_name = 'export/sample_form_export.html'
    filename = 'month_tax_report'

    context = {
        'title': 'خلاصه گزارش مالیات',
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

        context['form_content_template'] = 'export/tax_summary_report.html'
        context['right_header_template'] = 'export/sample_head.html'

        context.update(self.context)

        return context


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
            'now' : jdatetime.date.today(),
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
