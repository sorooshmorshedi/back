import pandas
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse

from payroll.lists.views import WorkshopListView, PersonnelListView, PersonnelFamilyListView, ContractRowListView, \
    ContractListView, WorkshopPersonnelListView
from payroll.models import Workshop, Personnel, PersonnelFamily, ContractRow, WorkshopPersonnel, Contract
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
            ['کد', 'نام', 'نام کارفرما', 'آدرس', 'نرخ بیمه سهم کارفرما', 'کد شعبه', 'نام شعبه',]
        ]
        for form in workshop:
            data.append([
                form.code,
                form.name,
                form.employer_name,
                form.address,
                form.employer_insurance_contribution,
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
                form.get_degree_of_education_dispaly(),
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
            ['کارگاه', 'پرسنل', 'ردیف پیمان', 'بیمه شده', 'تاریخ اضافه شدن به لیست بیمه', 'عنوان شغلی',
                'سابقه بیمه قبلی خارچ از کارگاه', 'سابقه بیمه قبلی در این کارگاه', 'سابقه بیمه جاری در این کارگاه',
                'مجموع سوابق بیمه ای', 'سمت', 'رسته شغلی', 'محل خدمت', ' وضعییت محل خدمت', 'نوع استخدام',
                'نوع قرارداد', 'وضعییت کارمند', 'تاریخ شروع قرارداد', 'تاریخ پایان قرارداد', 'تاریخ ترک کار']
        ]
        for form in workshop_personnel:
            data.append([
                form.workshop.name,
                form.personnel.full_name,
                form.contract_row,
                form.insurance,
                form.insurance_add_date,
                form.work_title,
                form.previous_insurance_history_out_workshop,
                form.previous_insurance_history_in_workshop,
                form.current_insurance_history_in_workshop,
                form.insurance_history_totality,
                form.job_position,
                form.job_group,
                form.job_location,
                form.job_location_status,
                form.get_employment_type_diplay(),
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
    def get_xlsx_data(contract: Contract):
        data = [
            [
                'لیست قرارداد ها'
            ],
            ['پرسنل در کارگاه', 'تاریخ شروع قرارداد', 'تاریخ پایان قرارداد', 'تاریخ ترک کار']
        ]
        for form in contract:
            data.append([
                form.workshop_personnel.title,
                form.contract_from_date,
                form.contract_to_date,
                form.quit_job_date
            ])
        return data



