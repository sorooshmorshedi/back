from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from helpers.auth import BasicCRUDPermission
from rest_framework import status
from rest_framework.response import Response

from helpers.models import is_valid_melli_code
from payroll.models import Workshop, Personnel, PersonnelFamily, ContractRow, Contract
from payroll.serializers import WorkShopSerializer, PersonnelSerializer, PersonnelFamilySerializer, \
    ContractRowSerializer, ContactSerializer


class WorkshopApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'workshop'

    def get(self, request):
        query = Workshop.objects.all()
        serializers = WorkShopSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkShopSerializer(data=request.data)
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
    permission_basename = 'workshop_personnel'

    def get(self, request):
        query = Contract.objects.all()
        serializers = ContactSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
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
        serializers = ContactSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ContactSerializer(query, data=request.data)
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

    def get(self, request, pk):
        personnel = Personnel.objects.get(pk=pk).first()
        if not personnel.name or not personnel.last_name:
            ValidationError(message="نام یا نام خانوادگی را وارد کنید")
        elif not personnel.father_name:
            ValidationError(message="نام پدر را وارد کنید")
        elif not personnel.country:
            ValidationError(message="کشور را وارد کنید")
        elif personnel.gender == 'f':
            personnel.military_service = 'x'
            personnel.save()
            ValidationError(message="کشور را وارد کنید")
        elif not personnel.national_code:
            ValidationError(message="کد ملی را وارد کنید")
        elif personnel.national_code:
            is_valid_melli_code(personnel.national_code)
        elif not personnel.identity_code:
            ValidationError(message="شماره شنانامه را وارد کنید")
        elif not personnel.date_of_birth:
            ValidationError(message="تاریخ تولذ را وارد کنید")
        elif not personnel.date_of_exportation:
            ValidationError(message="تاریخ صدور شناسنامه را وارد کنید")
        elif not personnel.location_of_birth:
            ValidationError(message="محل تولد شناسنامه را وارد کنید")
        elif not personnel.location_of_exportation:
            ValidationError(message="محل صدور شناسنامه را وارد کنید")
        elif not personnel.city_phone_code:
            ValidationError(message="کد تلفن شهر را وارد کنید")
        elif personnel.city_phone_code:
            city_phone_validator = RegexValidator(regex='^(0){1}[0-9]{2}$',
                                                  message='کد باید از سه عدد تشکیل شوذ و با صفر شروع شوذ',
                                                  code='nomatch')
            city_phone_validator(personnel.city_phone_code)
        elif not personnel.phone_number:
            ValidationError(message="تلفن را وارد کنید")
        elif not personnel.mobile_number_1:
            ValidationError(message="شماره موبایل را وارد کنید")
        elif personnel.mobile_number_1:
            length_validator = RegexValidator(regex='^.{11}$', message='طول شماره موبایل باید 11 رقم باشد',
                                              code='nomatch')
            format_validator = RegexValidator(regex='^(09){1}[0-9]{9}$', message='ساختار شماره موبایل صحیح نبست')
            length_validator(personnel.mobile_number_1)
            format_validator(personnel.mobile_number_1)
        elif personnel.mobile_number_2:
            length_validator = RegexValidator(regex='^.{11}$', message='طول شماره موبایل باید 11 رقم باشد',
                                              code='nomatch')
            format_validator = RegexValidator(regex='^(09){1}[0-9]{9}$', message='ساختار شماره موبایل صحیح نبست')
            length_validator(personnel.mobile_number_2)
            format_validator(personnel.mobile_number_2)
        elif not personnel.address:
            ValidationError(message="آدرس را وارد کنید")
        elif personnel.postal_code:
            postal_code_validator = RegexValidator(regex='^.{10}$', message='طول کد پستی باید 10 رقم باشد',
                                                   code='nomatch')
            postal_code_validator(personnel.postal_code)
        elif personnel.insurance and not personnel.insurance_code:
            ValidationError(message="َشماره بیمه را وارد کنید")
        elif personnel.degree_of_education == 'di':
            if not personnel.field_of_study:
                ValidationError(message="رشته تحصیلی را وارد کنید")
        elif personnel.degree_of_education != 'un':
            if not personnel.field_of_study:
                ValidationError(message="رشته تحصیلی را وارد کنید")
            elif not personnel.university_type:
                ValidationError(message="نوع دانشگاه را وارد کنید")
            elif not personnel.university_name:
                ValidationError(message="نام دانشگاه را وارد کنید")
        elif not personnel.account_bank_name:
            ValidationError(message="نام بانک حساب را وارد کنید")
        elif not personnel.account_bank_number:
            ValidationError(message="شماره حساب حقوق را وارد کنید")
        elif personnel.bank_cart_number:
            cart_number_validator = RegexValidator(regex='^.{16}$', message='طول شماره کارت باید 16 رقم باشد',
                                                   code='nomatch')
            cart_number_validator(personnel.bank_cart_number)
        elif personnel.sheba_number:
            sheba_validator = RegexValidator(regex='^.{24}$', message='طول شماره شبا باید 24 رقم باشد',
                                             code='nomatch')
            sheba_validator(personnel.sheba_number)
        else:
            personnel.is_personnel_verified = True
            personnel.save()
            return Response({'status': 'personnel verify done'}, status=status.HTTP_200_OK)
        return Response({'status': 'personnel verify failed'}, status=status.HTTP_417_EXPECTATION_FAILED)
