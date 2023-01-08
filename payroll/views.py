import jdatetime
from django.db.models import Q
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import datetime

from helpers.auth import BasicCRUDPermission
from rest_framework import status, generics
from rest_framework.response import Response

from payroll.functions import is_shenase_meli, is_valid_melli_code
from payroll.models import Workshop, Personnel, PersonnelFamily, ContractRow, WorkshopPersonnel, HRLetter, Contract, \
    LeaveOrAbsence, Mission, ListOfPay, ListOfPayItem, WorkshopTaxRow, WorkshopTax, Loan, OptionalDeduction, LoanItem, \
    Adjustment, WorkTitle
from payroll.serializers import WorkShopSerializer, PersonnelSerializer, PersonnelFamilySerializer, \
    ContractRowSerializer, WorkshopPersonnelSerializer, HRLetterSerializer, ContractSerializer, \
    LeaveOrAbsenceSerializer, MissionSerializer, ListOfPaySerializer, ListOfPayItemsAddInfoSerializer, \
    ListOfPayItemSerializer, WorkshopTaxRowSerializer, WorkShopSettingSerializer, \
    WorkShopTaxSerializer, LoanSerializer, DeductionSerializer, LoanItemSerializer, ListOfPayLessSerializer, \
    ListOfPayBankSerializer, ListOfPayItemPaySerializer, ListOfPayPaySerializer, ListOfPayItemAddPaySerializer, \
    ListOfPayCopyPaySerializer, AdjustmentSerializer, WorkTitleSerializer
from users.models import City


class WorkTitleListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'work_title'
    queryset = WorkTitle.objects.all()
    serializer_class = WorkTitleSerializer


class WorkTitleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'work_title'
    queryset = WorkTitle.objects.all()
    serializer_class = WorkTitleSerializer

class WorkTitleSearchApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'work_title'

    def get(self, request, search):
        print(search)
        query = WorkTitle.objects.filter(Q(code__icontains=search) | Q(name__icontains=search))
        serializers = WorkTitleSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

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


class ContractRowActiveApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get(self, request, pk):
        row = ContractRow.objects.get(pk=pk)
        row.status = True
        row.save()
        return Response({'وضعیت': ' فعال  کردن ردیف پیمان انجام شد'}, status=status.HTTP_200_OK)


class ContractRowUnActiveApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get(self, request, pk):
        row = ContractRow.objects.get(pk=pk)
        row.status = False
        row.save()
        return Response({'وضعیت': 'غیر فعال  کردن ردیف پیمان انجام شد'}, status=status.HTTP_200_OK)


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


class WorkshopPersonnelContractDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get(self, request, pk):
        query = Contract.objects.filter(Q(workshop_personnel=pk) & Q(is_verified=True))
        serializers = ContractSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


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
        query = HRLetter.objects.filter(Q(is_template='t') & Q(company=company) & Q(is_verified=True))
        serializers = HRLetterSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class HRActiveApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'hr_letter'

    def get(self, request, pk):
        hr = HRLetter.objects.get(pk=pk)
        for hr_letter in HRLetter.objects.filter(contract=hr.contract):
            hr_letter.is_active = False
            hr_letter.save()
        hr.is_active = True
        hr.save()
        return Response({'وضعیت': ' فعال  کردن حکم کارگزینی انجام شد'}, status=status.HTTP_200_OK)


class HRUnActiveApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract_row'

    def get(self, request, pk):
        hr = HRLetter.objects.get(pk=pk)
        hr.is_active = False
        hr.save()
        return Response({'وضعیت': 'غیر فعال  کردن ردیف حکم کارگزینی انجام شد'}, status=status.HTTP_200_OK)

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
            raise ValidationError('قراردادی ثبت نشده')
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
        data = request.data
        try:
            if data['ezafe_kari'] and data['ezafe_kari'] != '':
                ezafe_kari = data['ezafe_kari']
                ezafe_kari = ezafe_kari.split(':')
                ezafe_kari = round((int(ezafe_kari[0]) + (int(ezafe_kari[1]) / 60)), 6)
                data['ezafe_kari'] = ezafe_kari
            elif data['ezafe_kari'] == '':
                data['ezafe_kari'] = 0
        except:
            raise ValidationError('برای اضافه کاری یک ساعت صحیح وارد کنید')

        try:
            if data['tatil_kari'] and data['tatil_kari'] != '':
                tatil_kari = data['tatil_kari']
                tatil_kari = tatil_kari.split(':')
                tatil_kari = round((int(tatil_kari[0]) + (int(tatil_kari[1]) / 60)), 6)
                data['tatil_kari'] = tatil_kari
            elif data['tatil_kari'] == '':
                data['tatil_kari'] = 0
        except:
            raise ValidationError('برای تعطیل کاری یک ساعت صحیح وارد کنید')

        try:
            if data['kasre_kar'] and data['kasre_kar'] != '':
                kasre_kar = data['kasre_kar']
                kasre_kar = kasre_kar.split(':')
                kasre_kar = round((int(kasre_kar[0]) + (int(kasre_kar[1]) / 60)), 6)
                data['kasre_kar'] = kasre_kar
            elif data['kasre_kar'] == '':
                data['kasre_kar'] = 0
        except:
            raise ValidationError('برای کسر کار یک ساعت صحیح وارد کنید')

        try:
            if data['shab_kari'] and data['shab_kari'] != '':
                shab_kari = data['shab_kari']
                shab_kari = shab_kari.split(':')
                shab_kari = round((int(shab_kari[0]) + (int(shab_kari[1]) / 60)), 6)
                data['shab_kari'] = shab_kari
            elif data['shab_kari'] == '':
                data['shab_kari'] = 0
        except:
            raise ValidationError('برای شب کاری یک ساعت صحیح وارد کنید')

        serializer = ListOfPayItemsAddInfoSerializer(query, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
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


class ListOfPayUltimateApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'

    def post(self, request, pk):
        use_in_calculate = request.data['use_in_calculate']
        ultimate = request.data['ultimate']
        list_of_pay = ListOfPay.objects.get(pk=pk)
        list_of_pay.ultimate = ultimate
        list_of_pay.use_in_calculate = use_in_calculate
        list_of_pay.save()
        return Response({'وضعیت': 'قطعی  کردن لیست حقوق انجام شد'}, status=status.HTTP_200_OK)
