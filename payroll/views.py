
import jdatetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from rest_framework import status
from rest_framework.response import Response

from helpers.models import is_valid_melli_code
from payroll.models import Workshop, Personnel, PersonnelFamily, ContractRow, WorkshopPersonnel, HRLetter, Contract, \
    LeaveOrAbsence, Mission
from payroll.serializers import WorkShopSerializer, PersonnelSerializer, PersonnelFamilySerializer, \
    ContractRowSerializer, WorkshopPersonnelSerializer, HRLetterSerializer, ContractSerializer, \
    LeaveOrAbsenceSerializer, MissionSerializer
from users.models import User


class WorkshopApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request):
        query = Workshop.objects.all()
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

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonnelApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get(self, request):
        query = Personnel.objects.all()
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


class PersonnelDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get_object(self, pk):
        try:
            return Personnel.objects.get(pk=pk)
        except Personnel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = PersonnelSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = PersonnelSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request):
        query = Contract.objects.all()
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


class WorkshopPersonnelApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop_personnel'

    def get(self, request):
        query = WorkshopPersonnel.objects.all()
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

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonnelVerifyApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'
    validate_message = ''
    validate_status = True
    def get(self, request, pk):
        personnel = Personnel.objects.get(pk=pk)
        if personnel.gender == 'f':
            personnel.military_service = 'x'
        if not personnel.name or not personnel.last_name:
            self.validate_status = False
            print(1)
            raise ValidationError(message="نام یا نام خانوادگی را وارد کنید")
        if not personnel.father_name:
            print(2)
            self.validate_status = False
            raise ValidationError(message="نام پدر را وارد کنید")
        if not personnel.country:
            self.validate_status = False
            print(3)
            raise ValidationError(message="کشور را وارد کنید")
        if not personnel.national_code:
            self.validate_status = False
            print(4)
            raise ValidationError(message="کد ملی را وارد کنید")
        if personnel.national_code:
            is_valid_melli_code(personnel.national_code)
        if not personnel.identity_code:
            self.validate_status = False
            raise ValidationError(message="شماره شنانامه را وارد کنید")
        if not personnel.date_of_birth:
            self.validate_status = False
            raise ValidationError(message="تاریخ تولذ را وارد کنید")
        if not personnel.date_of_exportation:
            self.validate_status = False
            raise ValidationError(message="تاریخ صدور شناسنامه را وارد کنید")
        if not personnel.location_of_birth:
            self.validate_status = False
            raise ValidationError(message="محل تولد شناسنامه را وارد کنید")
        if not personnel.location_of_exportation:
            self.validate_status = False
            raise ValidationError(message="محل صدور شناسنامه را وارد کنید")
        if not personnel.city_phone_code:
            self.validate_status = False
            raise ValidationError(message="کد تلفن شهر را وارد کنید")
        if personnel.city_phone_code:
            city_phone_validator = RegexValidator(regex='^(0){1}[0-9]{2}$',
                                                  message='کد باید از سه عدد تشکیل شوذ و با صفر شروع شوذ',
                                                  code='nomatch')
            city_phone_validator(personnel.city_phone_code)
        if not personnel.phone_number:
            self.validate_status = False
            raise ValidationError(message="تلفن را وارد کنید")
        if not personnel.mobile_number_1:
            self.validate_status = False
            raise ValidationError(message="شماره موبایل را وارد کنید")
        if personnel.mobile_number_1:
            length_validator = RegexValidator(regex='^.{11}$', message='طول شماره موبایل باید 11 رقم باشد',
                                              code='nomatch')
            format_validator = RegexValidator(regex='^(09){1}[0-9]{9}$', message='ساختار شماره موبایل صحیح نبست')
            length_validator(personnel.mobile_number_1)
            format_validator(personnel.mobile_number_1)
        if personnel.mobile_number_2:
            length_validator = RegexValidator(regex='^.{11}$', message='طول شماره موبایل باید 11 رقم باشد',
                                              code='nomatch')
            format_validator = RegexValidator(regex='^(09){1}[0-9]{9}$', message='ساختار شماره موبایل صحیح نبست')
            length_validator(personnel.mobile_number_2)
            format_validator(personnel.mobile_number_2)
        if not personnel.address:
            self.validate_status = False
            raise ValidationError(message="آدرس را وارد کنید")
        if personnel.postal_code:
            postal_code_validator = RegexValidator(regex='^.{10}$', message='طول کد پستی باید 10 رقم باشد',
                                                   code='nomatch')
            postal_code_validator(personnel.postal_code)
        if personnel.insurance and not personnel.insurance_code:
            self.validate_status = False
            raise ValidationError(message="َشماره بیمه را وارد کنید")
        if personnel.degree_education == 'di':
            if not personnel.field_of_study:
                self.validate_status = False
                raise ValidationError(message="رشته تحصیلی را وارد کنید")
        if personnel.degree_education != 'un':
            if not personnel.field_of_study:
                self.validate_status = False
                raise ValidationError(message="رشته تحصیلی را وارد کنید")
            elif not personnel.university_type:
                self.validate_status = False
                raise ValidationError(message="نوع دانشگاه را وارد کنید")
            elif not personnel.university_name:
                self.validate_status = False
                raise ValidationError(message="نام دانشگاه را وارد کنید")
        if not personnel.account_bank_name:
            self.validate_status = False
            raise ValidationError(message="نام بانک حساب را وارد کنید")
        if not personnel.account_bank_number:
            self.validate_status = False
            raise ValidationError(message="شماره حساب حقوق را وارد کنید")
        if personnel.bank_cart_number:
            cart_number_validator = RegexValidator(regex='^.{16}$', message='طول شماره کارت باید 16 رقم باشد',
                                                   code='nomatch')
            cart_number_validator(personnel.bank_cart_number)
        if personnel.sheba_number:
            sheba_validator = RegexValidator(regex='^.{24}$', message='طول شماره شبا باید 24 رقم باشد',
                                             code='nomatch')
            sheba_validator(personnel.sheba_number)
        if self.validate_status:
            personnel.is_personnel_verified = True
            personnel.save()
            return Response({'status': 'personnel verify done'}, status=status.HTTP_200_OK)
        return Response({'status': 'personnel verify failed'}, status=status.HTTP_417_EXPECTATION_FAILED)


class HRLetterApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'hr_letter'

    def get(self, request):
        query = HRLetter.objects.all()
        serializers = HRLetterSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
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

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                if contract.quit_job_date and contract.quit_job_date.__gt__(from_date) and contract.quit_job_date.__lt__(to_date):
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


class SearchPersonnelByCode(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'personnel'

    def get(self, request, code):
        national_code = str(code)
        query = Personnel.objects.filter(Q(personnel_code=code) | Q(national_code=national_code)).first()
        serializers = PersonnelSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)


class PaymentList(APIView):
    months_day = {
        'fa': 31,
        'or': 31,
        'kh': 31,
        'ti': 31,
        'mo': 31,
        'sh': 31,
        'me': 30,
        'ab': 30,
        'az': 30,
        'de': 30,
        'ba': 30,
        'es': 29,
    }
    months = {
        'fa': 1,
        'or': 2,
        'kh': 3,
        'ti': 4,
        'mo': 5,
        'sh': 6,
        'me': 7,
        'ab': 8,
        'az': 9,
        'de': 10,
        'ba': 11,
        'es': 12,
    }

    def get(self, request, year, month, pk):
        month_days = self.months_day[month]
        month = self.months[month]
        start_date = jdatetime.date(year, month, 1, locale='fa_IR')
        end_date = jdatetime.date(year, month, month_days, locale='fa_IR')
        personnels = []
        contracts = []
        personnel_normal_worktime = {}
        workshop_personnel = WorkshopPersonnel.objects.filter(workshop_id=pk)

        workshop_contracts = Contract.objects.filter(workshop_personnel__in=workshop_personnel)
        for personnel in Personnel.objects.filter(workshop_personnel__in=workshop_personnel):
            personnel_normal_worktime[personnel.id] = 0
        for contract in workshop_contracts:
            if not contract.quit_job_date:
                end = contract.contract_to_date
            else:
                end = contract.quit_job_date
            if contract.contract_from_date.__le__(start_date) and end.__ge__(end_date):
                contracts.append(contract.id)
                personnel_normal_worktime[contract.workshop_personnel.personnel.id] += month_days
            if contract.contract_from_date.__ge__(start_date) and end.__le__(end_date):
                contracts.append(contract.id)
                personnel_normal_worktime[contract.workshop_personnel.personnel.id] +=\
                    end.day - contract.contract_from_date.day
            if contract.contract_from_date.__le__(start_date) and end.__gt__(start_date) and\
                    end.__lt__(end_date):
                contracts.append(contract.id)
                personnel_normal_worktime[contract.workshop_personnel.personnel.id] +=\
                    end.day
            if contract.contract_from_date.__ge__(start_date) and end.__ge__(end_date) and \
                    contract.contract_from_date.__lt__(end_date):
                contracts.append(contract.id)
                personnel_normal_worktime[contract.workshop_personnel.personnel.id] +=\
                    month_days - contract.contract_from_date.day + 1

        filtered_contracts = Contract.objects.filter(pk__in=contracts)

        for contract in filtered_contracts:
            personnels.append(contract.workshop_personnel.personnel.id)
        personnels = Personnel.objects.filter(Q(pk__in=personnels) & Q(is_personnel_active=True))
        filtered_workshops = WorkshopPersonnel.objects.filter(Q(personnel__in=personnels) & Q(workshop=pk))

        filtered_absence = LeaveOrAbsence.objects.filter(Q(workshop_personnel__in=filtered_workshops))

        filtered_absence = filtered_absence.filter(workshop_personnel__in=filtered_workshops)
        personnel_absence = filtered_absence.exclude(leave_type='e')

        response_data = []
        counter = 0
        for personnel in personnels:
            day_of_absence = 0
            for absence in personnel_absence.all():
                if absence.workshop_personnel.personnel == personnel:
                    if absence.from_date.__ge__(start_date) and absence.to_date.__le__(end_date):
                        day_of_absence += absence.time_period
                    elif absence.from_date.__lt__(start_date) and absence.to_date.__le__(end_date) and \
                            absence.to_date.__gt__(start_date):
                        day_of_absence += absence.to_date.day
                    elif absence.from_date.__gt__(start_date) and absence.to_date.__gt__(end_date) and \
                            absence.from_date.__le__(end_date):
                        day_of_absence += month_days - absence.from_date.day
                    elif absence.from_date.__le__(start_date) and absence.to_date.__ge__(end_date):
                        day_of_absence += month_days
            normal = personnel_normal_worktime[personnel.id]
            real_work = normal - int(day_of_absence)
            response_data.append(
                {
                    'row': counter,
                    'id': personnel.id,
                    'name': personnel.name + ' ' + personnel.last_name,
                    'normal_work': normal,
                    'real_work': real_work,
                }
            )
            counter += 1

        return Response(response_data, status=status.HTTP_200_OK)






