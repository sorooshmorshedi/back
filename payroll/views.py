import jdatetime
from django.db.models import Q
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import datetime

from helpers.auth import BasicCRUDPermission
from rest_framework import status
from rest_framework.response import Response

from payroll.functions import is_shenase_meli, is_valid_melli_code
from payroll.models import Workshop, Personnel, PersonnelFamily, ContractRow, WorkshopPersonnel, HRLetter, Contract, \
    LeaveOrAbsence, Mission, ListOfPay, ListOfPayItem, WorkshopTaxRow, WorkshopTax, Loan, OptionalDeduction, LoanItem, \
    Adjustment
from payroll.serializers import WorkShopSerializer, PersonnelSerializer, PersonnelFamilySerializer, \
    ContractRowSerializer, WorkshopPersonnelSerializer, HRLetterSerializer, ContractSerializer, \
    LeaveOrAbsenceSerializer, MissionSerializer, ListOfPaySerializer, ListOfPayItemsAddInfoSerializer, \
    ListOfPayItemSerializer, WorkshopTaxRowSerializer, WorkShopSettingSerializer, \
    WorkShopTaxSerializer, LoanSerializer, DeductionSerializer, LoanItemSerializer, ListOfPayLessSerializer, \
    ListOfPayBankSerializer, ListOfPayItemPaySerializer, ListOfPayPaySerializer, ListOfPayItemAddPaySerializer, \
    ListOfPayCopyPaySerializer, AdjustmentSerializer


# workshop APIs


class WorkshopApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request):
        company = request.user.active_company.pk
        data = request.data
        data['company'] = company
        query = Workshop.objects.filter(Q(company=company) & Q(is_active=True)& Q(is_verified=True))
        serializers = WorkShopSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        company = request.user.active_company.pk
        data = request.data
        data['company'] = company
        serializer = WorkShopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopDefaultApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request, pk):
        workshop = Workshop.objects.get(pk=pk)
        workshop.is_default = True
        workshop.save()
        return Response({workshop.name: workshop.is_default}, status=status.HTTP_200_OK)


class WorkshopUnDefaultApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request, pk):
        workshop = Workshop.objects.get(pk=pk)
        workshop.is_default = False
        workshop.save()
        return Response({workshop.name: workshop.is_default}, status=status.HTTP_200_OK)


class WorkshopGetDefaultApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request):
        company = request.user.active_company.pk
        query = Workshop.objects.filter(Q(company=company) & Q(is_active=True) &
                                        Q(is_verified=True) & Q(is_default=True))
        serializers = WorkShopSerializer(query.first())
        return Response(serializers.data, status=status.HTTP_200_OK)


class WorkshopDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get_object(self, pk):
        try:
            return Workshop.objects.get(pk=pk)
        except Workshop.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = WorkShopSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = WorkShopSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
            self.error_messages.append('وضعییت را وارد کنید')

        if self.validate_status:
            workshop.is_verified = True
            workshop.save()
            return Response({'وضعییت': 'ثبت نهایی کارگاه انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class WorkshopUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request, pk):
        workshop = Workshop.objects.get(pk=pk)
        workshop.is_verified = False
        workshop.save()
        return Response({'وضعییت': 'غیر نهایی  کردن کارگاه انجام شد'}, status=status.HTTP_200_OK)


class WorkshopContractRowsDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get_object(self, pk):
        try:
            return ContractRow.objects.filter(Q(workshop=pk) & Q(status=True) & Q(is_verified=True))
        except ContractRow.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ContractRowSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class WorkshopSettingDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get_object(self, pk):
        try:
            return Workshop.objects.get(pk=pk)
        except Workshop.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = WorkShopSettingSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = WorkShopSettingSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopTaxApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_tax'

    def get(self, request):
        company = request.user.active_company.pk
        query = WorkshopTax.objects.filter(company=company)
        serializers = WorkShopTaxSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        company = request.user.active_company.pk
        data = request.data
        data['company'] = company
        serializer = WorkShopTaxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopTaxDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_tax'

    def get_object(self, pk):
        try:
            return WorkshopTax.objects.get(pk=pk)
        except WorkshopTax.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = WorkShopTaxSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = WorkShopTaxSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkshopTaxRowApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_tax_row'

    def get(self, request):
        query = WorkshopTaxRow.objects.all()
        serializers = WorkshopTaxRowSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkshopTaxRowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopTaxRowDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_tax_row'

    def get_object(self, pk):
        try:
            return WorkshopTaxRow.objects.get(pk=pk)
        except WorkshopTaxRow.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = WorkshopTaxRowSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = WorkshopTaxRowSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# personnel APIs


class PersonnelApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get(self, request):
        company = request.user.active_company.pk
        query = Personnel.objects.filter(Q(company=company) & Q(is_personnel_active=True) &
                                         Q(is_personnel_verified=True))
        serializers = PersonnelSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        company = request.user.active_company.pk
        data = request.data
        data['company'] = company
        serializer = PersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonneNotInWorkshoplApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get(self, request, pk):
        company = request.user.active_company.pk
        query = Personnel.objects.filter(Q(company=company) & Q(is_personnel_active=True) &
                                         Q(is_personnel_verified=True))
        personnel = []
        for item in query:
            if not item.is_in_workshop(pk):
                personnel.append(item.id)
        query = query.filter(id__in=personnel)
        serializers = PersonnelSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class PersonnelDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get_object(self, pk):
        try:
            return Personnel.objects.get(pk=pk)
        except Personnel.DoesNotExist:
            raise Http404

    def edit_personnel(self, pk):
        person = self.get_object(pk)
        person.is_personnel_verified = False
        person.save()


    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = PersonnelSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        self.edit_personnel(pk)
        query = self.get_object(pk)
        serializer = PersonnelSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            self.error_messages.append("وضعییت پرسنل را وارد کنید")
        if self.validate_status:
            personnel.is_personnel_verified = True
            personnel.save()
            return Response({'وضعییت': 'ثبت نهایی پرسنل  انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class PersonnelUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get(self, request, pk):
        personnel = Personnel.objects.get(pk=pk)
        personnel.is_personnel_verified = False
        personnel.save()
        return Response({'status': 'personnel un verify done'}, status=status.HTTP_200_OK)


# personnel family APIs


class PersonnelFamilyApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel_family'

    def get(self, request):
        query = PersonnelFamily.objects.all()
        serializers = PersonnelFamilySerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PersonnelFamilySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonnelFamilyDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel_family'

    def get_object(self, pk):
        try:
            return PersonnelFamily.objects.get(pk=pk)
        except PersonnelFamily.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = PersonnelFamilySerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = PersonnelFamilySerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            self.error_messages.append("وضعییت تاهل را وارد کنید")
        if not personnel.study_status:
            self.validate_status = False
            self.error_messages.append("وضعییت تحصیل را وارد کنید")
        if not personnel.military_service:
            self.validate_status = False
            self.error_messages.append("خدمت سربازی را وارد کنید")
        if not personnel.physical_condition:
            self.validate_status = False
            self.error_messages.append("وضعییت جسمی را وارد کنید")
        if personnel.relative == 'f' or personnel.relative == 'm':
            same = PersonnelFamily.objects.filter(Q(personnel=personnel.personnel) & Q(relative=personnel.relative) &
                                                  Q(is_verified=True))
            if len(same) != 0:
                self.validate_status = False
                self.error_messages.append("این نسبت قبلا ثبت شده")

        if self.validate_status:
            personnel.is_verified = True
            personnel.save()
            return Response({'وضعییت': 'ثبت نهایی خانواده پرسنل  انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class PersonnelFamilyUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel_family'
    def get(self, request, pk):
        personnel = PersonnelFamily.objects.get(pk=pk)
        personnel.is_verified = False
        personnel.save()
        return Response({'status': 'personnel un verify done'}, status=status.HTTP_200_OK)


# contract row APIs


class ContractRowApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get(self, request):
        query = ContractRow.objects.all()
        serializers = ContractRowSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContractRowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractRowDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get_object(self, pk):
        try:
            return ContractRow.objects.get(pk=pk)
        except ContractRow.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ContractRowSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ContractRowSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractRowAdjustmentDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'adjustment'

    def get_object(self, pk):
        try:
            return Adjustment.objects.filter(contract_row=pk)
        except Adjustment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = AdjustmentSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


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
        if contract_row.from_date and contract_row.initial_to_date and\
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
            self.error_messages.append('وضعییت را وارد کنید')
        if self.validate_status:
            contract_row.is_verified = True
            contract_row.save()
            return Response({'وضعییت': 'ثبت نهایی ردیف پیمان انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class ContractRowUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'
    def get(self, request, pk):
        row = ContractRow.objects.get(pk=pk)
        row.is_verified = False
        row.save()
        return Response({'وضعییت': 'غیر نهایی  کردن ردیف پیمان انجام شد'}, status=status.HTTP_200_OK)


class ContractRowActiveApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get(self, request, pk):
        row = ContractRow.objects.get(pk=pk)
        row.status = True
        row.save()
        return Response({'وضعییت': ' فعال  کردن ردیف پیمان انجام شد'}, status=status.HTTP_200_OK)


class ContractRowUnActiveApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get(self, request, pk):
        row = ContractRow.objects.get(pk=pk)
        row.status = False
        row.save()
        return Response({'وضعییت': 'غیر فعال  کردن ردیف پیمان انجام شد'}, status=status.HTTP_200_OK)


class AdjustmentApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'adjustment'

    def get(self, request):
        company = request.user.active_company.pk
        workshops = Workshop.objects.filter(company=company)
        contract_rows = ContractRow.objects.filter(workshop__in=workshops)
        query = Adjustment.objects.filter(contract_row__in=contract_rows)
        serializers = AdjustmentSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdjustmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdjustmentDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'adjustment'

    def get_object(self, pk):
        try:
            return Adjustment.objects.get(pk=pk)
        except Adjustment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = AdjustmentSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = AdjustmentSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# workshop personnel APIs


class WorkshopPersonnelApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_personnel'

    def get(self, request):
        company = request.user.active_company
        workshops = company.workshop.all()
        query = WorkshopPersonnel.objects.filter(Q(workshop__in=workshops) & Q(is_verified=True))
        workshop_personnel = []
        for person in query:
            if not person.quit_job_date:
                workshop_personnel.append(person.id)
        query = WorkshopPersonnel.objects.filter(id__in=workshop_personnel)

        serializers = WorkshopPersonnelSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkshopPersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopPersonnelDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_personnel'

    def get_object(self, pk):
        try:
            return WorkshopPersonnel.objects.get(pk=pk)
        except WorkshopPersonnel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = WorkshopPersonnelSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = WorkshopPersonnelSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopAllPersonnelDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_personnel'

    def get(self, request, pk):
        query = WorkshopPersonnel.objects.filter(Q(workshop=pk) & Q(is_verified=True))
        serializers = WorkshopPersonnelSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


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
        if not personnel.work_title:
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
        if personnel.previous_insurance_history_out_workshop and\
            personnel.previous_insurance_history_out_workshop > 1000:
            self.validate_status = False
            self.error_messages.append("سابقه بیمه قبلی خارج این کارگاه نمیتواند بزرگتر از 1000 باشد")
        if personnel.previous_insurance_history_in_workshop and\
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
                                                          Q(personnel=personnel.personnel) &
                                                          Q(is_verified=True))
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
            return Response({'وضعییت': 'ثبت نهایی پرسنل کارگاه انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class WorkshopPersonnelUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_personnel'

    def get(self, request, pk):
        personnel = WorkshopPersonnel.objects.get(pk=pk)
        personnel.is_verified = False
        personnel.save()
        return Response({'status': 'personnel un verify done'}, status=status.HTTP_200_OK)


class SearchPersonnelByCode(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get_object(self, code, request):
        national_code = str(code)
        try:
            company = request.user.active_company.pk
            personnel = Personnel.objects.filter(Q(personnel_code=code) | Q(national_code=national_code) &
                                                 Q(company=company) & Q(is_personnel_verified=True) &
                                                 Q(is_personnel_active=True)).first()
            return Personnel.objects.get(pk=personnel.pk)
        except AttributeError:
            raise Http404

    def get(self, request, code):
        query = self.get_object(code, request)
        serializers = PersonnelSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)


# contract APIs


class ContractApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request):
        company = request.user.active_company
        workshop = company.workshop.all()
        workshop_personnel = WorkshopPersonnel.objects.filter(workshop__in=workshop)
        query = Contract.objects.filter(Q(workshop_personnel__in=workshop_personnel) & Q(is_verified=True))
        serializers = ContractSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ContractSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ContractSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                if contract.contract_from_date.__ge__(contract.quit_job_date):
                    self.validate_status = False
                    self.error_messages.append('تاریخ ترک کار باید بعد از  تاریخ شروع قرارداد باشد')
                if contract.quit_job_date.__ge__(contract.contract_to_date):
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
            if contract.insurance_add_date and contract.contract_from_date:
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

        if self.validate_status and contract.check_with_same:
            self.validate_status = False
            self.error_messages.append('در این زمان برای پرسنل قرارداد دیگری ثبت شده')

        if self.validate_status:
            contract.is_verified = True
            contract.save()
            return Response({'وضعییت': 'ثبت نهایی قرارداد انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class ContractUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'
    def get(self, request, pk):
        contract = Contract.objects.get(pk=pk)
        contract.is_verified = False
        contract.save()
        return Response({'وضعییت': 'غیر نهایی  کردن قرارداد انجام شد'}, status=status.HTTP_200_OK)

# Human Resource letter


class HRLetterApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'hr_letter'

    def get(self, request):
        query = HRLetter.objects.all()
        serializers = HRLetterSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        company = request.user.active_company.pk
        data = request.data
        data['company'] = company
        serializer = HRLetterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HRLetterDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'hr_letter'

    def get_object(self, pk):
        try:
            return HRLetter.objects.get(pk=pk)
        except HRLetter.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = HRLetterSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = HRLetterSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetHRLetterTemplatesApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'hr_letter'

    def get(self, request):
        company = request.user.active_company.pk
        query = HRLetter.objects.filter(Q(is_template='t') & Q(company=company))
        serializers = HRLetterSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

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

        if self.validate_status:
            hr.is_verified = True
            hr.save()
            return Response({'وضعییت': 'ثبت نهایی حکم کارگزینی انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class HRLUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'hr_letter'

    def get(self, request, pk):
        hr = HRLetter.objects.get(pk=pk)
        hr.is_verified = False
        hr.save()
        return Response({'وضعییت': 'غیر نهایی  کردن حکم کارگزینی انجام شد'}, status=status.HTTP_200_OK)

# Leave Or Absence APIs


class LeaveOrAbsenceApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'leave_or_absence'

    def get(self, request):
        query = LeaveOrAbsence.objects.all()
        serializers = LeaveOrAbsenceSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LeaveOrAbsenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveOrAbsenceDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'leave_or_absence'

    def get_object(self, pk):
        try:
            return LeaveOrAbsence.objects.get(pk=pk)
        except LeaveOrAbsence.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = LeaveOrAbsenceSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = LeaveOrAbsenceSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            return Response({'وضعییت': 'ثبت نهایی مرخصی انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class LeaveOrAbsenceUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'leave_or_absence'

    def get(self, request, pk):
        leave = LeaveOrAbsence.objects.get(pk=pk)
        leave.is_verified = False
        leave.save()
        return Response({'وضعییت': 'غیر نهایی  کردن مرخصی انجام شد'}, status=status.HTTP_200_OK)



# Mission APIs


class MissionApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'mission'

    def get(self, request):
        query = Mission.objects.all()
        serializers = MissionSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MissionDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'mission'

    def get_object(self, pk):
        try:
            return Mission.objects.get(pk=pk)
        except Mission.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = MissionSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = MissionSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class MissionUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'mission'

    def get(self, request, pk):
        mission = Mission.objects.get(pk=pk)
        mission.is_verified = False
        mission.save()
        return Response({'وضعییت': 'غیر نهایی  کردن ماموریت انجام شد'}, status=status.HTTP_200_OK)




# Loan APIs


class LoanApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'loan'

    def get(self, request):
        query = Loan.objects.all()
        serializers = LoanSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'loan'

    def get_object(self, pk):
        try:
            return Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = LoanSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = LoanSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonnelLoanDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'loan'

    def get_object(self, pk):
        try:
            return Loan.objects.filter(workshop_personnel=pk)
        except Loan.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = LoanSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class LoanItemDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'loan_item'

    def get_object(self, pk):
        try:
            return LoanItem.objects.get(pk=pk)
        except LoanItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = LoanItemSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = LoanItemSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if not loan.episode:
            self.validate_status = False
            self.error_messages.append('تعداد اقساط را وارد کنید')
        if loan.episode == 0:
            self.validate_status = False
            self.error_messages.append('تعداد اقساط بزرگتر از صفر باشد ')


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
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class LoanUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'loan'

    def get(self, request, pk):
        loan = Loan.objects.get(pk=pk)
        loan.is_verified = False
        loan.save()
        return Response({'وضعییت': 'غیر نهایی  کردن مساعده یا وام انجام شد'}, status=status.HTTP_200_OK)

# Deduction APIs


class DeductionApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'


    def get(self, request):
        company = request.user.active_company.pk
        data = request.data
        data['company'] = company
        query = OptionalDeduction.objects.filter(company=company)
        serializers = DeductionSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        company = request.user.active_company.pk
        data = request.data
        data['company'] = company
        serializer = DeductionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeductionDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'

    def get_object(self, pk):
        try:
            return OptionalDeduction.objects.get(pk=pk)
        except OptionalDeduction.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = DeductionSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = DeductionSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TemplateDeductionDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'

    def get(self, request):
        query = OptionalDeduction.objects.filter(is_template=True)
        serializers = DeductionSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class PersonnelDeductionDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'

    def get_object(self, pk):
        try:
            return OptionalDeduction.objects.filter(workshop_personnel=pk)
        except OptionalDeduction.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = DeductionSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


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

        if self.validate_status:
            deductions.is_verified = True
            deductions.save()
            return Response({'وضعییت': 'ثبت نهایی کسورات اختیاری انجام شد'}, status=status.HTTP_200_OK)
        else:
            counter = 1
            response = []
            for error in self.error_messages:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعییت': response}, status=status.HTTP_400_BAD_REQUEST)


class DeductionUnVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'

    def get(self, request, pk):
        deductions = OptionalDeduction.objects.get(pk=pk)
        deductions.is_verified = False
        deductions.save()
        return Response({'وضعییت': 'غیر نهایی  کردن کسورات اختیاری انجام شد'}, status=status.HTTP_200_OK)

# payroll APIs

class ListOfPayApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'

    def get(self, request):
        query = ListOfPay.objects.all()
        serializers = ListOfPaySerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class ListOfPayDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'

    def get_object(self, pk):
        try:
            return ListOfPay.objects.get(pk=pk)
        except ListOfPay.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ListOfPaySerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ListOfPayItemDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay_item'

    def get_object(self, pk):
        try:
            return ListOfPayItem.objects.get(list_of_pay=pk)
        except ListOfPayItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ListOfPayItemSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ListOfPayLessDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'

    def get_object(self, pk):
        try:
            return ListOfPay.objects.get(pk=pk)
        except ListOfPay.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ListOfPayLessSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)


class WorkshopListOfPayApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'

    def get(self, request, pk, month, year):
        query = ListOfPay.objects.filter(Q(workshop=pk) & Q(month=month) & Q(year=int(year)))
        serializers = ListOfPayCopyPaySerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class PaymentVerifyApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request, year, month, pk):
        date = jdatetime.date(year, month, 1, locale='fa_IR')
        workshop = Workshop.objects.get(pk=pk)
        verify_tax_row = workshop.get_tax_row(date)
        verify_personnel = workshop.get_personnel
        error = False
        error_response = {}
        if not verify_tax_row:
            error = True
            error_response['ردیف مالیات'] = 'موجود نیست'
        if len(verify_personnel) == 0:
            error = True
            error_response['پرسنل فعال'] = 'موجود نیست'
        if error:
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'وضعیت': 'چک شد'}, status=status.HTTP_200_OK)


class PaymentList(APIView):
    months_day = {
        1: 31,
        2: 31,
        3: 31,
        4: 31,
        5: 31,
        6: 31,
        7: 30,
        8: 30,
        9: 30,
        10: 30,
        11: 30,
        12: 29,
    }

    def post(self, request, year, month, pk):
        month_days = self.months_day[month]
        start_date = jdatetime.date(year, month, 1, locale='fa_IR')
        end_date = jdatetime.date(year, month, month_days, locale='fa_IR')
        workshop = Workshop.objects.get(pk=pk)
        data = request.data
        payroll_list = ListOfPay.objects.create(workshop=workshop, year=year, month=month, name=data['name'],
                                                use_in_calculate=data['use_in_calculate'], ultimate=data['ultimate'],
                                                    month_days=month_days, start_date=start_date, end_date=end_date)
        contract = payroll_list.get_contracts
        if len(contract) == 0:
            raise ValidationError('no contract')
        else:
            payroll_list.save()
            response = payroll_list.info_for_items
            for item in response:
                if item['insurance']:
                    insurance = 'y'
                else:
                    insurance = 'n'

                payroll_list_item = ListOfPayItem.objects.create(
                    list_of_pay=payroll_list,
                    workshop_personnel=WorkshopPersonnel.objects.filter(Q(workshop=pk) & Q(personnel_id=item['pk'])).first(),
                    contract=Contract.objects.get(pk=item['contract']),
                    normal_worktime=item['normal_work'],
                    real_worktime=item['real_work'],
                    mission_day=item['mission'],
                    is_insurance=insurance,
                    absence_day=item['leaves']['a'],
                    entitlement_leave_day=item['leaves']['e'],
                    daily_entitlement_leave_day=item['leaves']['ed'],
                    hourly_entitlement_leave_day=item['leaves']['eh'],
                    illness_leave_day=item['leaves']['i']+item['leaves']['c'],
                    without_salary_leave_day=item['leaves']['w'],
                    matter_47_leave_day=item['leaves']['m']
                )
                payroll_list_item.save()
            list_of_pay = payroll_list
            list_of_pay_serializers = ListOfPaySerializer(list_of_pay)
            return Response(list_of_pay_serializers.data, status=status.HTTP_200_OK)


class CalculationsPayrollDetail(APIView):

    def get(self, pk,  request):
        try:
            workshop_personnel = WorkshopPersonnel.objects.get(pk=pk)
            contracts = Contract.objects.filter(workshop_personnel=workshop_personnel)
        except(LeaveOrAbsence.DoesNotExist, WorkshopPersonnel.DoesNotExist):
            raise Http404
        data = request.GET
        period_from_date = data['from_date']
        period_to_date = data['to_date']
        from_date = jdatetime.datetime.strptime(period_from_date, '%d/%m/%Y')
        to_date = jdatetime.datetime.strptime(period_to_date, '%d/%m/%Y')
        months_days = {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 30, 8: 30, 9: 30, 10: 30, 11: 30, 12: 29}
        normal_job_time = None
        for contract in contracts:
            if not contract.quit_job_date:
                if contract.contract_from_date.__le__(from_date) and contract.contract_to_date.__ge__(to_date)\
                        and contract.contract_from_date.__le__(to_date):
                    normal_job_time = months_days[from_date.month]
                elif contract.contract_from_date.__ge__(from_date) and contract.contract_to_date.__ge__(to_date):
                    normal_job_time = months_days[from_date.month] - from_date.day + 1
                elif contract.contract_from_date.__le__(from_date) and contract.contract_to_date.__le__(to_date)\
                        and contract.contract_to_date.__gt__(from_date):
                    normal_job_time = contract.contract_from_date.day
                elif contract.contract_from_date.__gt__(from_date) and contract.contract_to_date.__lt__(to_date):
                    normal_job_time = contract.contract_to_date.day - contract.contract_from_date.day
            else:
                if contract.quit_job_date and contract.quit_job_date.__gt__(from_date)\
                        and contract.quit_job_date.__lt__(to_date):
                    if contract.contract_from_date.__le__(from_date) and contract.contract_to_date.__ge__(to_date):
                        normal_job_time = contract.quit_job_date.day
                    elif contract.contract_from_date.__ge__(from_date) and contract.contract_to_date.__ge__(to_date)\
                            and contract.contract_from_date.__le__(to_date):
                        normal_job_time =contract.quit_job_date.day - contract.contract_from_date.day
                    elif contract.contract_from_date.__le__(from_date) and contract.contract_to_date.__le__(to_date)\
                            and contract.contract_to_date.__gt__(from_date):
                        normal_job_time = contract.quit_job_date.day
                    elif contract.contract_from_date.__gt__(from_date) and contract.contract_to_date.__lt__(to_date):
                        normal_job_time = contract.quit_job_date.day - contract.contract_from_date.day
        return Response({'normal_job_time': normal_job_time}, status=status.HTTP_200_OK)


class PayAPI(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay_item'

    def get_object(self, pk):
        try:
            return ListOfPayItem.objects.get(pk=pk)
        except ListOfPayItem.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ListOfPayItemPaySerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayItemDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay_item'

    def get_object(self, pk):
        try:
            return ListOfPayItem.objects.get(pk=pk)
        except ListOfPayItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ListOfPayItemSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ListOfPayItemsCalculate(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay_item'

    def get_object(self, pk):
        try:
            return ListOfPayItem.objects.get(pk=pk)
        except ListOfPayItem.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ListOfPayItemsAddInfoSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOfPayBankDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'
    def get_object(self, pk):
        try:
            return ListOfPay.objects.get(pk=pk)
        except ListOfPay.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ListOfPayBankSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ListOfPayPaymentAPI(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'

    def get_object(self, pk):
        try:
            return ListOfPay.objects.get(pk=pk)
        except ListOfPay.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ListOfPayPaySerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ListOfPayPaySerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOfPayItemPaymentAPI(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay_item'

    def get_object(self, pk):
        try:
            return ListOfPayItem.objects.get(pk=pk)
        except ListOfPayItem.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ListOfPayItemAddPaySerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOfPayCopy(APIView):
    months_day = {
        1: 31,
        2: 31,
        3: 31,
        4: 31,
        5: 31,
        6: 31,
        7: 30,
        8: 30,
        9: 30,
        10: 30,
        11: 30,
        12: 29,
    }
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'
    def get_object(self, pk):
        try:
            return ListOfPay.objects.get(pk=pk)
        except ListOfPay.DoesNotExist:
            raise Http404

    def post(self, request, pk):

        list_of_pay = self.get_object(pk)
        items = ListOfPayItem.objects.filter(list_of_pay=pk)
        data = request.data
        new_list_of_pay = list_of_pay
        new_list_of_pay.id = None
        new_list_of_pay.name = data['name']
        new_list_of_pay.year = data['year']
        new_list_of_pay.month = data['month']
        new_list_of_pay.month_days = self.months_day[data['month']]
        new_list_of_pay.start_dat = jdatetime.date(data['year'],
                                                  data['month'],
                                                  1,
                                                  locale='fa_IR')
        new_list_of_pay.end_date = jdatetime.date(data['year'],
                                                  data['month'],
                                                  self.months_day[data['month']],
                                                  locale='fa_IR')
        new_list_of_pay.save()

        for item in items:
            new_item = item
            new_item.id = None
            new_item.list_of_pay = ListOfPay.objects.get(pk=new_list_of_pay.id)
            new_item.save()
        return Response({'id': list_of_pay.id}, status=status.HTTP_201_CREATED)
