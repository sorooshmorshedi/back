from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from helpers.auth import BasicCRUDPermission
from payroll.functions import is_valid_melli_code, is_shenase_meli
from payroll.models import Workshop, WorkshopTax, Personnel, PersonnelFamily, ContractRow, WorkshopPersonnel, Contract, \
    HRLetter, LeaveOrAbsence, Mission, Loan, OptionalDeduction


class WorkshopVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        workshop = Workshop.objects.get(pk=pk)

        if not workshop.workshop_code:
            self.validate_status = False
            self.error_messages.append('کد کارگاه را وارد کنید')
        if workshop.workshop_code and len(workshop.workshop_code) != 10:
            self.validate_status = False
            self.error_messages.append('کد کارگاه باید 10 رقمی باشد')
        if not workshop.name:
            self.validate_status = False
            self.error_messages.append('نام کارگاه را وارد کنید')
        if not workshop.employer_name:
            self.validate_status = False
            self.error_messages.append('نام کارفرما را وارد کنید')
        if not workshop.postal_code:
            self.validate_status = False
            self.error_messages.append('کد پستی کارگاه را وارد کنید')
        if workshop.postal_code and len(workshop.postal_code) != 10:
            self.validate_status = False
            self.error_messages.append('کد پستی کارگاه باید 10 رقمی باشد')
        if not workshop.address:
            self.validate_status = False
            self.error_messages.append('آدرس کارگاه را وارد کنید')
        if workshop.is_active == None:
            self.validate_status = False
            self.error_messages.append('وضعیت را وارد کنید')

        # workshop setting verify

        if not workshop.worker_insurance_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ حق بیمه سهم بیمه شده را تنظیمات کارگاه وارد کنید')

        if not workshop.employee_insurance_nerkh:
            self.validate_status = False
            self.error_messages.append(' نرخ حق بیمه سهم کارفرما را تنظیمات کارگاه وارد کنید')

        if not workshop.unemployed_insurance_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ حق بیمه سهم بیکاری را تنظیمات کارگاه وارد کنید')

        if not workshop.ezafe_kari_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ اضافه کاری را تنظیمات کارگاه وارد کنید')

        if not workshop.tatil_kari_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ تعطیل کاری را تنظیمات کارگاه وارد کنید')

        if not workshop.kasre_kar_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ کسر کار را تنظیمات کارگاه وارد کنید')

        if not workshop.shab_kari_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ شب کاری را تنظیمات کارگاه وارد کنید')

        if not workshop.aele_mandi_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ عائله مندی را تنظیمات کارگاه وارد کنید')

        if not workshop.nobat_kari_sob_asr_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ نوبت کاری صبح و عصر را تنظیمات کارگاه وارد کنید')

        if not workshop.nobat_kari_sob_shab_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ نوبت کاری صبح و شب را تنظیمات کارگاه وارد کنید')

        if not workshop.nobat_kari_asr_shab_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ نوبت کاری عصر و شب را تنظیمات کارگاه وارد کنید')

        if not workshop.nobat_kari_sob_asr_shab_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ نوبت کاری صبح و عصر و شب را تنظیمات کارگاه وارد کنید')

        if not workshop.nobat_kari_sob_asr_shab_nerkh:
            self.validate_status = False
            self.error_messages.append('نرخ نوبت کاری صبح و عصر و شب را تنظیمات کارگاه وارد کنید')

        if self.validate_status:
            workshop.is_verified = True
            workshop.save()
            return Response({'وضعیت': 'ثبت نهایی کارگاه انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class WorkshopUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request, pk):
        workshop = Workshop.objects.get(pk=pk)
        workshop.is_verified = False
        workshop.save()
        return Response({'وضعیت': 'غیر نهایی  کردن کارگاه انجام شد'}, status=status.HTTP_200_OK)


class WorkshopTaxRowVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_tax'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        workshop_tax = WorkshopTax.objects.get(pk=pk)

        if not workshop_tax.name:
            self.validate_status = False
            self.error_messages.append('نام جدول معاف مالیات را وارد کنید')

        if not workshop_tax.from_date:
            self.validate_status = False
            self.error_messages.append(' " از تاریخ " جدول معاف مالیات را وارد کنید')

        if not workshop_tax.to_date:
            self.validate_status = False
            self.error_messages.append(' " تا تاریخ " جدول معاف مالیات را وارد کنید')

        if self.validate_status:
            workshop_tax.is_verified = True
            workshop_tax.save()
            print(workshop_tax)
            return Response({'وضعیت': 'ثبت نهایی جدول معاف مالیات کارگاه انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class WorkshopTaxRowUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_tax'

    def get(self, request, pk):
        workshop_tax = WorkshopTax.objects.get(pk=pk)
        workshop_tax.is_verified = False
        workshop_tax.save()
        return Response({'وضعیت': 'غیر نهایی  کردن جدول معاف مالیات کارگاه انجام شد'}, status=status.HTTP_200_OK)


class PersonnelVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        company = request.user.active_company.pk
        personnel = Personnel.objects.get(pk=pk)
        if personnel.gender == 'f':
            personnel.military_service = 'x'
        if not personnel.name or not personnel.last_name:
            self.validate_status = False
            self.error_messages.append("نام یا نام خانوادگی را وارد کنید")
        if not personnel.father_name:
            self.validate_status = False
            self.error_messages.append("نام پدر را وارد کنید")
        if not personnel.nationality:
            self.validate_status = False
            self.error_messages.append("ملیت را وارد کنید")
        if personnel.nationality == 1:
            personnel.country = 'ایران'
        if not personnel.country:
            self.validate_status = False
            self.error_messages.append("کشور را وارد کنید")
        if not personnel.gender:
            self.validate_status = False
            self.error_messages.append("جنسیت را وارد کنید")
        if personnel.gender != 'f' and not personnel.military_service and personnel.nationality != 2:
            self.validate_status = False
            self.error_messages.append("وضعییت خدمت سربازی را وارد کنید")
        if not personnel.identity_code and personnel.nationality != 2:
            self.validate_status = False
            self.error_messages.append("شماره شناسنامه را وارد کنید")
        if not personnel.national_code and personnel.nationality != 2:
            self.validate_status = False
            self.error_messages.append("کد ملی را وارد کنید")
        if not personnel.national_code and personnel.nationality == 2:
            self.validate_status = False
            self.error_messages.append("کد فراگیر تابعیت را وارد کنید")
        if personnel.national_code:
            same_code = Personnel.objects.filter(Q(national_code=personnel.national_code) & Q(company=company) &
                                                 Q(is_personnel_verified=True) & Q(is_personnel_verified=True))
            if personnel.nationality == 1:
                is_valid, message = is_valid_melli_code(personnel.national_code)
                if not is_valid:
                    self.validate_status = False
                    self.error_messages.append(message)
                if len(same_code) > 0:
                    self.validate_status = False
                    self.error_messages.append("کد ملی تکراری می باشد")
            if personnel.nationality == 2 and len(same_code) > 0:
                self.validate_status = False
                self.error_messages.append("کد فراگیر تابعیت تکراری می باشد")
        if not personnel.marital_status:
            self.validate_status = False
            self.error_messages.append("وضعیت تاهل را وارد کنید")
        if not personnel.date_of_birth:
            self.validate_status = False
            self.error_messages.append("تاریخ تولد را وارد کنید")
        if not personnel.date_of_exportation and personnel.nationality != 2:
            self.validate_status = False
            self.error_messages.append("تاریخ صدور شناسنامه را وارد کنید")
        if not personnel.location_of_birth and personnel.nationality != 2:
            self.validate_status = False
            self.error_messages.append("محل تولد  را وارد کنید")
        if not personnel.location_of_foreign_birth and personnel.nationality == 2:
            self.validate_status = False
            self.error_messages.append("محل تولد  را وارد کنید")
        if not personnel.location_of_exportation and personnel.nationality != 2:
            self.validate_status = False
            self.error_messages.append("محل صدور شناسنامه را وارد کنید")
        if not personnel.city:
            self.validate_status = False
            self.error_messages.append("شهر محل سکونت را وارد کنید")
        if not personnel.address:
            self.validate_status = False
            self.error_messages.append("آدرس را وارد کنید")
        if not personnel.postal_code:
            self.validate_status = False
            self.error_messages.append("کد پستی را وارد کنید")
        if personnel.postal_code:
            if len(personnel.postal_code) > 10 or len(personnel.postal_code) < 10:
                self.validate_status = False
                self.error_messages.append("طول کد پستی باید 10 رقم باشد")
        if personnel.city_phone_code:
            if len(personnel.city_phone_code) != 3:
                self.validate_status = False
                self.error_messages.append("کد تلفن شهر باید سه رقمی باشد")
            if personnel.city_phone_code[0] != '0':
                self.validate_status = False
                self.error_messages.append("کد تلفن شهر باید با صفر شروع شود")
        if personnel.phone_number and len(personnel.phone_number) != 8:
            self.validate_status = False
            self.error_messages.append("تلفن شهر باید 8 رقمی باشد")
        if not personnel.mobile_number_1:
            self.validate_status = False
            self.error_messages.append("شماره موبایل را وارد کنید")
        if personnel.mobile_number_1:
            if len(personnel.mobile_number_1) > 11 or len(personnel.mobile_number_1) < 11:
                self.validate_status = False
                self.error_messages.append("طول شماره موبایل باید 11 رقم باشد")
            if personnel.mobile_number_1[0] != '0':
                self.validate_status = False
                self.error_messages.append("شماره موبایل با صفر شروع میشود")
        if personnel.mobile_number_2:
            if len(personnel.mobile_number_2) > 11 or len(personnel.mobile_number_2) < 11:
                self.validate_status = False
                self.error_messages.append("طول شماره موبایل 2 باید 11 رقم باشد")
            if personnel.mobile_number_2[0] != '0':
                self.validate_status = False
                self.error_messages.append("شماره موبایل 2 با صفر شروع میشود")
        if personnel.insurance and not personnel.insurance_code:
            self.validate_status = False
            self.error_messages.append("َشماره بیمه را وارد کنید")
        if personnel.insurance_code:
            if len(personnel.insurance_code) > 10 or len(personnel.insurance_code) < 10:
                self.validate_status = False
                self.error_messages.append("طول شماره بیمه باید 10 رقم باشد")
            if personnel.insurance_code[:2] != '00':
                self.validate_status = False
                self.error_messages.append("شماره بیمه باید با 00 شروع شود")
        if not personnel.degree_education:
            self.validate_status = False
            self.error_messages.append("مدرک تحصیلی را وارد کنید")
        if personnel.degree_education and personnel.degree_education >= 3:
            if not personnel.field_of_study:
                self.validate_status = False
                self.error_messages.append("رشته تحصیلی را وارد کنید")
            if personnel.degree_education > 3 and not personnel.university_type:
                self.validate_status = False
                self.error_messages.append("نوع دانشگاه را وارد کنید")
            if personnel.degree_education > 3 and not personnel.university_name:
                self.validate_status = False
                self.error_messages.append("نام دانشگاه را وارد کنید")
        if not personnel.account_bank_name:
            self.validate_status = False
            self.error_messages.append("نام بانک حساب را وارد کنید")
        if not personnel.account_bank_number:
            self.validate_status = False
            self.error_messages.append("شماره حساب حقوق را وارد کنید")
        if not personnel.bank_cart_number:
            self.validate_status = False
            self.error_messages.append("شماره کارت حقوق را وارد کنید")
        if personnel.bank_cart_number and len(personnel.bank_cart_number) != 16:
            self.validate_status = False
            self.error_messages.append("طول شماره کارت باید 16 رقم باشد")
        if not personnel.sheba_number:
            self.validate_status = False
            self.error_messages.append("شماره شبا حقوق را وارد کنید")
        if personnel.sheba_number and len(personnel.sheba_number) != 24:
            self.validate_status = False
            self.error_messages.append("طول شماره شبا باید 24 رقم باشد")
        if personnel.is_personnel_active == None:
            self.validate_status = False
            self.error_messages.append("وضعیت پرسنل را وارد کنید")
        if self.validate_status:
            personnel.is_personnel_verified = True
            personnel.save()
            return Response({'وضعیت': ''}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class PersonnelUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get(self, request, pk):
        personnel = Personnel.objects.get(pk=pk)
        personnel.is_personnel_verified = False
        personnel.save()
        return Response({'وضعیت': 'غیر نهایی  کردن پرسنل  انجام شد'}, status=status.HTTP_200_OK)


class PersonnelFamilyVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel_family'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        personnel = PersonnelFamily.objects.get(pk=pk)
        if not personnel.relative:
            self.validate_status = False
            self.error_messages.append("نسبت وارد کنید")
        if not personnel.name or not personnel.last_name:
            self.validate_status = False
            self.error_messages.append("نام یا نام خانوادگی را وارد کنید")
        if not personnel.national_code:
            self.validate_status = False
            self.error_messages.append("کد ملی را وارد کنید")
        if personnel.national_code:
            is_valid, message = is_valid_melli_code(personnel.national_code)
            if not is_valid:
                self.validate_status = False
                self.error_messages.append(message)
            same_code = PersonnelFamily.objects.filter(Q(personnel=personnel.personnel.id) & Q(is_verified=True) &
                                                       Q(national_code=personnel.national_code))
            if len(same_code) > 0:
                self.validate_status = False
                self.error_messages.append("کد ملی تکراری می باشد")
            if personnel.national_code == personnel.personnel.national_code:
                self.validate_status = False
                self.error_messages.append("کد ملی با پرسنل برابر می باشد")
        if not personnel.date_of_birth:
            self.validate_status = False
            self.error_messages.append("تاریخ تولد را وارد کنید")
        if not personnel.marital_status:
            self.validate_status = False
            self.error_messages.append("وضعیت تاهل را وارد کنید")
        if not personnel.study_status:
            self.validate_status = False
            self.error_messages.append("وضعیت تحصیل را وارد کنید")
        if not personnel.military_service:
            self.validate_status = False
            self.error_messages.append("خدمت سربازی را وارد کنید")
        if not personnel.physical_condition:
            self.validate_status = False
            self.error_messages.append("وضعیت جسمی را وارد کنید")
        if personnel.is_active == None:
            self.validate_status = False
            self.error_messages.append("وضعیت را وارد کنید")
        if personnel.relative == 'f' or personnel.relative == 'm':
            same = PersonnelFamily.objects.filter(Q(personnel=personnel.personnel) & Q(relative=personnel.relative) &
                                                  Q(is_verified=True))
            if len(same) != 0:
                self.validate_status = False
                self.error_messages.append("این نسبت قبلا ثبت شده")

        if self.validate_status:
            personnel.is_verified = True
            personnel.save()
            return Response({'وضعیت': 'ثبت نهایی خانواده پرسنل  انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class PersonnelFamilyUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel_family'

    def get(self, request, pk):
        personnel = PersonnelFamily.objects.get(pk=pk)
        personnel.is_verified = False
        personnel.save()
        return Response({'وضعیت': 'غیر نهایی شدن خانواده پرسنل  انجام شد'}, status=status.HTTP_200_OK)


class ContractRowVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contracct_row'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        contract_row = ContractRow.objects.get(pk=pk)
        if not contract_row.contract_row:
            self.validate_status = False
            self.error_messages.append('ردیف پیمان را وارد کنید')
        if contract_row.contract_row and len(contract_row.contract_row) < 3:
            row = '0' * (3 - len(contract_row.contract_row))
            new_row = row + contract_row.contract_row
            contract_row.contract_row = new_row
        if not contract_row.contract_number:
            self.validate_status = False
            self.error_messages.append('شماره قرارداد را وارد کنید')
        if not contract_row.registration_date:
            self.validate_status = False
            self.error_messages.append('تاریخ قرارداد را وارد کنید')
        if not contract_row.from_date:
            self.validate_status = False
            self.error_messages.append('تاریخ شروع را وارد کنید')
        if not contract_row.initial_to_date:
            self.validate_status = False
            self.error_messages.append('تاریخ پایان را وارد کنید')
        if contract_row.from_date and contract_row.initial_to_date and \
                contract_row.from_date > contract_row.initial_to_date:
            self.validate_status = False
            self.error_messages.append('تاریخ شروع قرارداد نمیتواند بزرگتر از تاریخ پایان قرارداد باشد')
        if not contract_row.assignor_national_code:
            self.validate_status = False
            self.error_messages.append('شناسه ملی واگذارکننده را وارد کنید')
        if contract_row.assignor_national_code:
            confirm, message = is_shenase_meli(contract_row.assignor_national_code)
            if not confirm:
                self.validate_status = False
                self.error_messages.append(message)

        if not contract_row.assignor_name:
            self.validate_status = False
            self.error_messages.append('نام واگذارکننده را وارد کنید')
        if not contract_row.assignor_workshop_code:
            self.validate_status = False
            self.error_messages.append('کد کارگاه واگذارکننده را وارد کنید')
        if contract_row.assignor_workshop_code and len(contract_row.assignor_workshop_code) != 10:
            self.validate_status = False
            self.error_messages.append('کد کارگاه واگذارکننده باید 10 رقمی باشد')
        if not contract_row.contract_initial_amount:
            self.validate_status = False
            self.error_messages.append('مبلغ اولیه قرارداد را وارد کنید')
        if contract_row.status == None:
            self.validate_status = False
            self.error_messages.append('وضعیت را وارد کنید')
        if self.validate_status:
            contract_row.is_verified = True
            contract_row.save()
            return Response({'وضعیت': 'ثبت نهایی ردیف پیمان انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class ContractRowUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get(self, request, pk):
        row = ContractRow.objects.get(pk=pk)
        row.is_verified = False
        row.save()
        return Response({'وضعیت': 'غیر نهایی  کردن ردیف پیمان انجام شد'}, status=status.HTTP_200_OK)


class WorkshopPersonnelVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_personnel'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        personnel = WorkshopPersonnel.objects.get(pk=pk)
        if not personnel.title:
            self.validate_status = False
            self.error_messages.append('عنوان شغلی(بیمه) را وارد کنید')
        if not personnel.job_location:
            self.validate_status = False
            self.error_messages.append("محل را خدمت")
        if not personnel.employee_status:
            self.validate_status = False
            self.error_messages.append("وضعیت کارمند را وارد کنید")
        if not personnel.job_location_status:
            self.validate_status = False
            self.error_messages.append("وضعیت محل کار را وارد کنید")
        if personnel.personnel.insurance == True:
            if personnel.previous_insurance_history_out_workshop == None:
                self.validate_status = False
                self.error_messages.append("سابقه بیمه قبلی خارج این کارگاه را وارد کنید")
            if personnel.previous_insurance_history_in_workshop == None:
                self.validate_status = False
                self.error_messages.append("سابقه بیمه قبلی در این کارگاه را وارد کنید")
        if personnel.previous_insurance_history_out_workshop and \
                personnel.previous_insurance_history_out_workshop > 1000:
            self.validate_status = False
            self.error_messages.append("سابقه بیمه قبلی خارج این کارگاه نمیتواند بزرگتر از 1000 باشد")
        if personnel.previous_insurance_history_in_workshop and \
                personnel.previous_insurance_history_in_workshop > 1000:
            self.validate_status = False
            self.error_messages.append("سابقه بیمه قبلی در این کارگاه نمیتواند بزرگتر از 1000 باشد")
        if not personnel.job_position:
            self.validate_status = False
            self.error_messages.append("سمت یا شغل (دارایی) را وارد کنید")
        if personnel.job_group == None:
            self.validate_status = False
            self.error_messages.append("رسته شغلی را وارد کنید")
        if not personnel.employment_type:
            self.validate_status = False
            self.error_messages.append("نوع استخدام را وارد کنید")
        if not personnel.contract_type:
            self.validate_status = False
            self.error_messages.append("نوع قرارداد را وارد کنید")
        if not personnel.employment_date:
            self.validate_status = False
            self.error_messages.append("تاریخ استخدام را وارد کنید")
        if personnel.sanavat_btn and not personnel.sanavat_previuos_days:
            self.validate_status = False
            self.error_messages.append("روز های کارکرد قبل از تعریف را وارد کنید")
        if personnel.sanavat_btn and not personnel.sanavat_previous_amount:
            self.validate_status = False
            self.error_messages.append("مبلغ حق سنوات شناسایی شده را وارد کنید")
        if personnel.sanavat_previuos_days and int(personnel.sanavat_previuos_days) >= 20000:
            self.validate_status = False
            self.error_messages.append("روز های کارکرد قبل از تعریف باید کوچک تر از 20000 باشد")
        same_personnel = WorkshopPersonnel.objects.filter(Q(workshop=personnel.workshop) &
                                                          Q(personnel=personnel.personnel) & Q(is_verified=True))
        quit = []
        for same_person in same_personnel:
            if same_person.quit_job_date:
                quit.append(same_person)
        if len(same_personnel) - len(quit) > 0:
            self.validate_status = False
            self.error_messages.append("این انتصاب تکراری است")
        if self.validate_status:
            personnel.is_verified = True
            personnel.save()
            return Response({'وضعیت': 'ثبت نهایی پرسنل کارگاه انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class WorkshopPersonnelUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_personnel'

    def get(self, request, pk):
        personnel = WorkshopPersonnel.objects.get(pk=pk)
        personnel.is_verified = False
        for contract in personnel.contract.all():
            contract.is_verified = False
            contract.save()
        personnel.save()
        return Response({'وضعیت': 'personnel un verify done'}, status=status.HTTP_200_OK)


class ContractVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contracct'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        contract = Contract.objects.get(pk=pk)
        if not contract.workshop_personnel:
            self.validate_status = False
            self.error_messages.append('پرسنل در کارگاه نمی تواند خالی باشد')
        if contract.workshop_personnel.is_verified == False:
            self.validate_status = False
            self.error_messages.append('پرسنل در کارگاه نهایی نیست')
        if not contract.code:
            self.validate_status = False
            self.error_messages.append('شماره قرارداد نمی تواند خالی باشد')
        if not contract.contract_from_date:
            self.validate_status = False
            self.error_messages.append('تاریخ شروع را وارد کنید')
        if not contract.contract_to_date:
            self.validate_status = False
            self.error_messages.append('تاریخ پایان را وارد کنید')
        sign_date = contract.workshop_personnel.employment_date
        if self.validate_status and contract.contract_from_date.__lt__(sign_date):
            self.validate_status = False
            self.error_messages.append('تاریخ شروع قرارداد باید بعد از تاریخ استخدام باشد')
        if self.validate_status and contract.contract_from_date.__ge__(contract.contract_to_date):
            self.validate_status = False
            self.error_messages.append('تاریخ شروع قرارداد باید قبل از  تاریخ پایان قرارداد باشد')
        if self.validate_status and contract.quit_job_date:
            if contract.contract_from_date.__gt__(contract.quit_job_date):
                self.validate_status = False
                self.error_messages.append('تاریخ ترک کار باید بعد از  تاریخ شروع قرارداد باشد')
            if contract.quit_job_date.__gt__(contract.contract_to_date):
                self.validate_status = False
                self.error_messages.append('تاریخ ترک کار باید قبل از  تاریخ پایان قرارداد باشد')
        if contract.insurance == True:
            if not contract.insurance_add_date:
                self.validate_status = False
                self.error_messages.append('تاریخ اضافه شدن به لیست بیمه را وارد کنید')
            if contract.insurance_add_date and contract.contract_from_date:
                if contract.contract_from_date.__gt__(contract.insurance_add_date):
                    self.validate_status = False
                    self.error_messages.append('تاریخ اضافه شدن به لیست بیمه باید بعد از تاریخ شروع قرارداد باشد')
            if contract.insurance_add_date and contract.contract_to_date:
                if contract.insurance_add_date.__gt__(contract.contract_to_date):
                    self.validate_status = False
                    self.error_messages.append('تاریخ اضافه شدن به لیست بیمه باید قبل از تاریخ پایان قرارداد باشد')
            if contract.workshop_personnel.personnel.insurance == False:
                if not contract.insurance_number:
                    self.validate_status = False
                    self.error_messages.append('شماره بیمه را وارد کنید')
                elif contract.insurance_number:
                    if len(contract.insurance_number) != 10:
                        self.validate_status = False
                        self.error_messages.append("طول شماره بیمه باید 10 رقم باشد")
                    if contract.insurance_number[:2] != '00':
                        self.validate_status = False
                        self.error_messages.append("شماره بیمه باید با 00 شروع شود")
            if self.validate_status:
                contract.workshop_personnel.insurance_add_date = contract.insurance_add_date
                contract.workshop_personnel.save()
                contract.workshop_personnel.personnel.insurance = True
                contract.workshop_personnel.personnel.insurance_code = contract.insurance_number
                contract.workshop_personnel.personnel.save()

        if contract.tax == True:
            if not contract.tax_add_date:
                self.validate_status = False
                self.error_messages.append('تاریخ اضافه شدن به لیست مالیات حقوق را وارد کنید')
            if contract.tax_add_date and contract.contract_from_date:
                if contract.contract_from_date.__gt__(contract.tax_add_date):
                    self.validate_status = False
                    self.error_messages.append('تاریخ اضافه شدن به لیست مالیات حقوق باید بعد از تاریخ شروع قرارداد باشد')
            if contract.tax_add_date and contract.contract_to_date:
                if contract.tax_add_date.__gt__(contract.contract_to_date):
                    self.validate_status = False
                    self.error_messages.append('تاریخ اضافه شدن به لیست مالیات حقوق باید قبل از تاریخ پایان قرارداد باشد')


        if self.validate_status and contract.check_with_same:
            self.validate_status = False
            self.error_messages.append('در این زمان برای پرسنل قرارداد دیگری ثبت شده')

        if self.validate_status:
            contract.is_verified = True
            contract.save()
            return Response({'وضعیت': 'ثبت نهایی قرارداد انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class ContractUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request, pk):
        contract = Contract.objects.get(pk=pk)
        contract.is_verified = False
        contract.save()
        return Response({'وضعیت': 'غیر نهایی  کردن قرارداد انجام شد'}, status=status.HTTP_200_OK)


class HRLVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'hr_letter'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        hr = HRLetter.objects.get(pk=pk)
        if not hr.is_template:
            self.validate_status = False
            self.error_messages.append('نوع حکم کارگزینی را  وارد کنید')

        elif hr.is_template == 't':
            hr.contract, hr.pay_done = None, False
            if not hr.name:
                self.validate_status = False
                self.error_messages.append('برای قالب حکم کارگزینی خود نام وارد کنید')
        else:
            if not hr.contract:
                self.validate_status = False
                self.error_messages.append('قرارداد را وارد کنید')

        if hr.hoghooghe_roozane_amount and not hr.hoghooghe_roozane_nature:
            self.validate_status = False
            self.error_messages.append('برای حداقل مزد روزانه، ماهیت عناوین شغلی را وارد کنید')

        if hr.paye_sanavat_amount and not hr.paye_sanavat_nature:
            self.validate_status = False
            self.error_messages.append('برای پایه سنوات روزانه، ماهیت عناوین شغلی را وارد کنید')

        if hr.haghe_maskan_amount and not hr.haghe_maskan_nature:
            self.validate_status = False
            self.error_messages.append('برای حق مسکن ، ماهیت عناوین شغلی را وارد کنید')

        if hr.bon_kharo_bar_amount and not hr.bon_kharo_bar_nature:
            self.validate_status = False
            self.error_messages.append('برای بن خوار و بار  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.haghe_sarparasti_amount and not hr.haghe_sarparasti_nature:
            self.validate_status = False
            self.error_messages.append('برای حق سرپرستی  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.haghe_modiriyat_amount and not hr.haghe_modiriyat_nature:
            self.validate_status = False
            self.error_messages.append('برای حق مدیریت  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.haghe_jazb_amount and not hr.haghe_jazb_nature:
            self.validate_status = False
            self.error_messages.append('برای حق جذب  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.fogholade_shoghl_amount and not hr.fogholade_shoghl_nature:
            self.validate_status = False
            self.error_messages.append('برای فوق العاده شغل  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.haghe_tahsilat_amount and not hr.haghe_tahsilat_nature:
            self.validate_status = False
            self.error_messages.append('برای حق تحصیلات  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.fogholade_sakhti_kar_amount and not hr.fogholade_sakhti_kar_nature:
            self.validate_status = False
            self.error_messages.append('برای فوق العاده سختی کار  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.haghe_ankal_amount and not hr.haghe_ankal_nature:
            self.validate_status = False
            self.error_messages.append('برای حق آنکال  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.fogholade_badi_abohava_amount and not hr.fogholade_badi_abohava_nature:
            self.validate_status = False
            self.error_messages.append('برای فوق العاده بدی هوا  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.mahroomiat_tashilat_zendegi_amount and not hr.mahroomiat_tashilat_zendegi_nature:
            self.validate_status = False
            self.error_messages.append('برای محرومیت از تسهیلات  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.fogholade_mahal_khedmat_amount and not hr.fogholade_mahal_khedmat_nature:
            self.validate_status = False
            self.error_messages.append('برای فوق العاده محل خدمت  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.fogholade_sharayet_mohit_kar_amount and not hr.fogholade_sharayet_mohit_kar_nature:
            self.validate_status = False
            self.error_messages.append('برای فوق العاده محیط کار  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.ayabo_zahab_amount and not hr.ayabo_zahab_nature:
            self.validate_status = False
            self.error_messages.append('برای ایاب و ذهاب  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.yarane_ghaza_amount and not hr.yarane_ghaza_nature:
            self.validate_status = False
            self.error_messages.append('برای یارانه غذا  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.haghe_shir_amount and not hr.haghe_shir_nature:
            self.validate_status = False
            self.error_messages.append('برای حق شیر  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.haghe_taahol_amount and not hr.haghe_taahol_nature:
            self.validate_status = False
            self.error_messages.append('برای حق تاهل  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.komakhazine_mahdekoodak_amount and not hr.komakhazine_mahdekoodak_nature:
            self.validate_status = False
            self.error_messages.append('برای کمک هزینه مهدکودک  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.komakhazine_varzesh_amount and not hr.komakhazine_varzesh_nature:
            self.validate_status = False
            self.error_messages.append('برای کمک هزینه ورزش  ، ماهیت عناوین شغلی را وارد کنید')

        if hr.komakhazine_mobile_amount and not hr.komakhazine_mobile_nature:
            self.validate_status = False
            self.error_messages.append('برای کمک هزینه موبایل  ، ماهیت عناوین شغلی را وارد کنید')

        if self.validate_status:
            hr.is_verified = True
            hr.save()
            return Response({'وضعیت': 'ثبت نهایی حکم کارگزینی انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class HRLUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'hr_letter'

    def get(self, request, pk):
        hr = HRLetter.objects.get(pk=pk)
        hr.is_verified = False
        hr.is_active = False
        hr.save()
        return Response({'وضعیت': 'غیر نهایی  کردن حکم کارگزینی انجام شد'}, status=status.HTTP_200_OK)


class LeaveOrAbsenceVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'leave_or_absence'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        leave = LeaveOrAbsence.objects.get(pk=pk)

        if not leave.leave_type:
            self.validate_status = False
            self.error_messages.append("نوع را مشخص کنید")
        elif leave.leave_type == 'e':
            if not leave.entitlement_leave_type:
                self.validate_status = False
                self.error_messages.append("نوع مرخصی استحقاقی را مشخص کنید")
            if leave.entitlement_leave_type == 'h':
                if not leave.date:
                    self.validate_status = False
                    self.error_messages.append("برای مرخصی ساعتی،  تاریخ را وارد کنید")
                if not leave.from_hour:
                    self.validate_status = False
                    self.error_messages.append("برای مرخصی ساعتی ، ساعت شروع را وارد کنید")
                if not leave.to_hour:
                    self.validate_status = False
                    self.error_messages.append("برای مرخصی ساعتی ، ساعت پایان را وارد کنید")
                if leave.from_hour.__gt__(leave.to_hour) and self.validate_status:
                    self.validate_status = False
                    self.error_messages.append("ساعت شروع نمیتواند از ساعت پایان بزرگتر باشد")
            elif leave.entitlement_leave_type == 'd':
                if not leave.from_date or not leave.to_date:
                    self.validate_status = False
                    self.error_messages.append("برای مرخصی روزانه، تاریخ شروع و پایان را وارد کنید")

        elif leave.leave_type == 'm':
            if not leave.matter73_leave_type:
                self.validate_status = False
                self.error_messages.append("دلیل مرخصی ماده 73 را مشخص کنید")
            if not leave.to_date or not leave.from_date:
                self.validate_status = False
                self.error_messages.append("تاریخ شروع و پایان را وارد کنید")

        elif leave.leave_type == 'i':
            if not leave.from_date or not leave.to_date:
                self.validate_status = False
                self.error_messages.append("برای مرخصی استعلاجی تاریخ شروع و پایان را وارد کنید")
            if not leave.cause_of_incident:
                self.validate_status = False
                self.error_messages.append("برای مرخصی استعلاجی علت حادثه را وارد کنید")

        elif leave.leave_type == 'w' or leave.leave_type == 'a' or leave.leave_type == 'c':
            if not leave.from_date or not leave.to_date:
                self.validate_status = False
                self.error_messages.append("تاریخ شروع و پایان را وارد کنید")

        if self.validate_status and leave.entitlement_leave_type != 'h' and leave.from_date.__gt__(leave.to_date):
            self.validate_status = False
            self.error_messages.append("تاریخ شروع نمیتواند از تاریخ پایان بزرگتر باشد")

        if self.validate_status and leave.entitlement_leave_type == 'h':
            if leave.to_hour.hour < 8 and leave.to_hour.hour > 0:
                self.validate_status = False
                self.error_messages.append("ساعت پایان باید قبل 00:00 بامداد بعد از 08:00 صبح باشد")

        if self.validate_status:
            is_same = leave.check_with_same
            if is_same:
                self.validate_status = False
                self.error_messages.append("در این زمان برای این پرسنل مرخصی یا غیبت  ثبت شده است")

        if self.validate_status:
            is_same_leave = leave.check_with_same_mission
            if is_same_leave:
                self.validate_status = False
                self.error_messages.append("در این زمان برای این پرسنل ماموریت ثبت شده است")

        if self.validate_status:
            check_with_contract = leave.check_with_contract
            if not check_with_contract:
                self.validate_status = False
                self.error_messages.append("در این زمان برای این پرسنل قرارداد ثبت نشده است")

        if self.validate_status:
            leave.is_verified = True
            leave.save()
            return Response({'وضعیت': 'ثبت نهایی مرخصی انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class LeaveOrAbsenceUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'leave_or_absence'

    def get(self, request, pk):
        leave = LeaveOrAbsence.objects.get(pk=pk)
        leave.is_verified = False
        leave.save()
        return Response({'وضعییت': 'غیر نهایی  کردن مرخصی انجام شد'}, status=status.HTTP_200_OK)


class MissionVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'mission'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        mission = Mission.objects.get(pk=pk)

        if mission.mission_type == 'h':
            mission.from_date, mission.to_date, = None, None
            if not mission.from_hour or not mission.to_hour or not mission.date:
                self.validate_status = False
                self.error_messages.append("برای ماموریت ساعتی، ساعت شروع و پایان و تاریخ را وارد کنید")
        else:
            mission.date, mission.from_hour, mission.to_hour = None, None, None
            if not mission.from_date or not mission.to_date:
                self.validate_status = False
                self.error_messages.append("برای ماموریت روزانه تاریح شروع و پایان را وارد کنید")
        if mission.from_date and mission.to_date and mission.from_date.__gt__(mission.to_date):
            self.validate_status = False
            self.error_messages.append("تاریح شروع نمیتواند از تاریخ پایان بزرگتر باشد")
        if mission.from_hour and mission.to_hour and mission.from_hour.__gt__(mission.to_hour):
            self.validate_status = False
            self.error_messages.append("ساعت شروع نمیتواند از ساعت پایان بزرگتر باشد")

        if self.validate_status:
            is_same = mission.check_with_same
            if is_same:
                self.validate_status = False
                self.error_messages.append("در این زمان برای این پرسنل ماموریت ثبت شده است")

        if self.validate_status:
            is_same_leave = mission.check_with_same_leave
            if is_same_leave:
                self.validate_status = False
                self.error_messages.append("در این زمان برای این پرسنل مرخصی یا غیبت ثبت شده است")

        if self.validate_status:
            check_with_contract = mission.check_with_contract
            if not check_with_contract:
                self.validate_status = False
                self.error_messages.append("در این زمان برای این پرسنل قرارداد ثبت نشده است")

        if self.validate_status:
            mission.is_verified = True
            mission.save()
            return Response({'وضعییت': 'ثبت نهایی ماموریت انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class MissionUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'mission'

    def get(self, request, pk):
        mission = Mission.objects.get(pk=pk)
        mission.is_verified = False
        mission.save()
        return Response({'وضعیت': 'غیر نهایی  کردن ماموریت انجام شد'}, status=status.HTTP_200_OK)


class LoanVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'loan'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        loan = Loan.objects.get(pk=pk)
        if not loan.loan_type:
            self.validate_status = False
            self.error_messages.append('نوع را وارد کنید')
        if not loan.pay_date:
            self.validate_status = False
            self.error_messages.append('تاریخ را وارد کنید')
        if not loan.amount:
            self.validate_status = False
            self.error_messages.append('مبلغ را وارد کنید')
        if loan.amount == 0:
            self.validate_status = False
            self.error_messages.append('مبلغ  باید بزرگتر از صفر باشد ')
        if loan.loan_type == 'd':
            loan.episode = 1
        if not loan.episode and loan.loan_type == 't':
            self.validate_status = False
            self.error_messages.append('تعداد اقساط را وارد کنید')
        if loan.episode == 0:
            self.validate_status = False
            self.error_messages.append('تعداد اقساط بزرگتر از صفر باشد ')

        if self.validate_status:
            check_with_contract = loan.check_with_contract
            if not check_with_contract:
                self.validate_status = False
                self.error_messages.append("در این زمان برای این پرسنل قرارداد ثبت نشده است")

        if self.validate_status:
            loan.is_verified = True
            loan.save()
            return Response({'وضعییت': 'ثبت نهایی مساعده یا وام انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class LoanUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'loan'

    def get(self, request, pk):
        loan = Loan.objects.get(pk=pk)
        loan.is_verified = False
        loan.save()
        return Response({'وضعیت': 'غیر نهایی  کردن مساعده یا وام انجام شد'}, status=status.HTTP_200_OK)


class DeductionVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'
    validate_status = True
    error_messages = []

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get(self, request, pk):
        deductions = OptionalDeduction.objects.get(pk=pk)
        if deductions.is_template == None:
            self.validate_status = False
            self.error_messages.append('نوع را وارد کنید')

        if deductions.is_template:
            deductions.workshop_personnel = None
            if not deductions.template_name:
                self.validate_status = False
                self.error_messages.append('نام قالب را وارد کنید')

        if not deductions.is_template:
            deductions.template_name = None
            if not deductions.workshop_personnel:
                self.validate_status = False
                self.error_messages.append('پرسنل  را وارد کنید')
            if not deductions.name:
                self.validate_status = False
                self.error_messages.append('نام کسورات  را وارد کنید')
        if not deductions.amount:
            self.validate_status = False
            self.error_messages.append('مبلغ  را وارد کنید')
        if deductions.amount == 0:
            self.validate_status = False
            self.error_messages.append('مبلغ  باید بزرگتر از صفر باشد ')
        if not deductions.episode:
            self.validate_status = False
            self.error_messages.append('تعداد ماه  را وارد کنید')
        if deductions.episode == 0:
            self.validate_status = False
            self.error_messages.append('تعداد ماه  باید بزرگتر از صفر باشد ')

        if not deductions.start_date and not deductions.is_template:
            self.validate_status = False
            self.error_messages.append('تاریخ  را وارد کنید')

        if self.validate_status and not deductions.is_template:
            check_with_contract = deductions.check_with_contract
            if not check_with_contract:
                self.validate_status = False
                self.error_messages.append("در این زمان برای این پرسنل قرارداد ثبت نشده است")

        if self.validate_status:
            deductions.is_verified = True
            deductions.save()
            return Response({'وضعیت': 'ثبت نهایی کسورات اختیاری انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


class DeductionUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'

    def get(self, request, pk):
        deductions = OptionalDeduction.objects.get(pk=pk)
        deductions.is_verified = False
        deductions.save()
        return Response({'وضعیت': 'غیر نهایی  کردن کسورات اختیاری انجام شد'}, status=status.HTTP_200_OK)
