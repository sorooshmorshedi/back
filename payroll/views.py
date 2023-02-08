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
    ListOfPayCopyPaySerializer, AdjustmentSerializer, WorkTitleSerializer, ListOfPayEditSerializer, \
    ContractEditSerializer, ContractEditInsuranceSerializer, ContractEditTaxSerializer
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
        query = WorkTitle.objects.filter(Q(code__icontains=search) | Q(name__icontains=search))
        serializers = WorkTitleSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class WorkTitleApiView(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'work_title'

    def get_object(self, pk):
        try:
            return WorkTitle.objects.get(pk=pk)
        except WorkTitle.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = WorkTitleSerializer(query)
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
        save_leave_limit = data['save_leave_limit']
        if not save_leave_limit:
            data['save_leave_limit'] = 0
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
        data = request.data
        save_leave_limit = data['save_leave_limit']
        if not save_leave_limit:
            data['save_leave_limit'] = 0
        serializer = WorkShopSerializer(query, data)
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
        data = request.data
        save_leave_limit = data['save_leave_limit']
        if not save_leave_limit:
            data['save_leave_limit'] = 0
        serializer = WorkshopPersonnelSerializer(query, data)
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
        return Response({'وضعیت': 'غیر فعال کردن ردیف حکم کارگزینی انجام شد'}, status=status.HTTP_200_OK)

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
        if not data['episode']:
            data['episode'] = 0
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
        data = request.data
        if not data['episode']:
            data['episode'] = 0
        serializer = DeductionSerializer(query, data=data)
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
        company = request.user.active_company.pk
        data = request.data
        data['company'] = company

        query = OptionalDeduction.objects.filter(Q(is_template=True) & Q(company=company))
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


class DeductionActiveApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'

    def get(self, request, pk):
        deduction = OptionalDeduction.objects.get(pk=pk)
        deduction.is_active = True
        deduction.save()
        return Response({'وضعیت': ' فعال  کردن کسورات اختیاری انجام شد'}, status=status.HTTP_200_OK)


class DeductionUnActiveApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'deductions'

    def get(self, request, pk):
        deduction = OptionalDeduction.objects.get(pk=pk)
        deduction.is_active = False
        deduction.save()
        return Response({'وضعیت': 'غیر فعال  کردن کسورات اختیاری انجام شد'}, status=status.HTTP_200_OK)

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

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def __init__(self):
        self.validate_status = True
        self.error_message = []

    def post(self, request, year, month, pk):
        month_days = self.months_day[month]
        start_date = jdatetime.date(year, month, 1, locale='fa_IR')
        end_date = jdatetime.date(year, month, month_days, locale='fa_IR')
        workshop = Workshop.objects.get(pk=pk)
        data = request.data

        if not data['name']:
            self.validate_status = False
            self.error_message.append('نام لیست را وارد کنید')
        if data['use_in_calculate'] == None:
            self.validate_status = False
            self.error_message.append('وضعیت محاسبه بیمه و مالیات را وارد کنید')

        if self.validate_status:
            payroll_list = ListOfPay.objects.create(workshop=workshop, year=year, month=month, name=data['name'],
                                                    use_in_calculate=data['use_in_calculate'],
                                                    use_in_bime=data['use_in_bime'], month_days=month_days,
                                                    start_date=start_date, end_date=end_date)

            contracts = payroll_list.get_contracts
            if contracts == 0:
                self.validate_status = False
                self.error_message.append('در این کارگاه و این زمان قراردادی ثبت نشده')
                payroll_list.delete()
            else:
                response = payroll_list.info_for_items
                for person in response:
                    contract = Contract.objects.get(pk=person['contract']),
                    if not contract[0].check_hr_letter:
                        self.validate_status = False
                        self.error_message.append('برای حداقل یک قرارداد حکم کارگزینی فعال موجود نیست')
                if self.validate_status:
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
        if not self.validate_status:
            counter = 1
            response = []
            for error in self.error_message:
                error = str(counter) + '-' + error
                counter += 1
                response.append(error)
            return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)


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
                        normal_job_time = contract.quit_job_date.day - 1
                    elif contract.contract_from_date.__ge__(from_date) and contract.contract_to_date.__ge__(to_date)\
                            and contract.contract_from_date.__le__(to_date):
                        normal_job_time = contract.quit_job_date.day - contract.contract_from_date.day
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

    def __init__(self):
        self.error_messages = []
        self.validate_status = True

    def get_object(self, pk):
        try:
            return ListOfPayItem.objects.get(pk=pk)
        except ListOfPayItem.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        query = self.get_object(pk)
        data = request.data
        days = query.list_of_pay.month_days
        is_in = request.data['is_in']
        notice = request.data['notice']
        del(data['is_in'])
        del(data['notice'])
        if is_in or notice:
            if not data['nobat_kari_sob_asr']:
                data['nobat_kari_sob_asr'] = 0
            if not data['nobat_kari_sob_shab']:
                data['nobat_kari_sob_shab'] = 0
            if not data['nobat_kari_asr_shab']:
                data['nobat_kari_asr_shab'] = 0
            if not data['nobat_kari_sob_asr_shab']:
                data['nobat_kari_sob_asr_shab'] = 0

            nobat_kari = int(data['nobat_kari_sob_asr']) + int(data['nobat_kari_sob_shab']) +\
                         int(data['nobat_kari_asr_shab']) + int(data['nobat_kari_sob_asr_shab'])

            if not data['sayer_ezafat']:
                data['sayer_ezafat'] = 0
            if not data['mazaya_gheyr_mostamar']:
                data['mazaya_gheyr_mostamar'] = 0
            if not data['hazine_made_137']:
                data['hazine_made_137'] = 0
            if not data['kosoorat_insurance']:
                data['kosoorat_insurance'] = 0
            if not data['sayer_moafiat']:
                data['sayer_moafiat'] = 0
            if not data['manategh_tejari_moafiat']:
                data['manategh_tejari_moafiat'] = 0
            if not data['ejtenab_maliat_mozaaf']:
                data['ejtenab_maliat_mozaaf'] = 0
            if not data['sayer_kosoorat']:
                data['sayer_kosoorat'] = 0
            if not data['cumulative_absence']:
                data['cumulative_absence'] = 0
            if not data['cumulative_mission']:
                data['cumulative_mission'] = 0
            if not data['cumulative_entitlement']:
                data['cumulative_entitlement'] = 0
            if not data['cumulative_illness']:
                data['cumulative_illness'] = 0
            if not data['cumulative_without_salary']:
                data['cumulative_without_salary'] = 0

            cumulative = int(data['cumulative_without_salary']) + int(data['cumulative_illness']) + \
                         int(data['cumulative_entitlement']) + int(data['cumulative_absence']) +\
                         int(data['cumulative_mission'])

            cumulative += int(query.mission_day)
            cumulative += int(query.without_salary_leave_day)
            cumulative += int(query.illness_leave_day)
            cumulative += int(query.absence_day)
            cumulative += int(query.entitlement_leave_day)

            if nobat_kari > days:
                self.validate_status = False
                self.error_messages.append('جمع نوبت کاری نمیتواند بزرگتر از تعداد روز های ماه باشد')

            if cumulative > days:
                self.validate_status = False
                self.error_messages.append('جمع موارد تجمیعی نمیتواند بزرگتر از تعداد روز های ماه باشد')

            try:
                if ':' not in data['ezafe_kari']:
                    data['ezafe_kari'] = int(data['ezafe_kari'])
                elif data['ezafe_kari'] and data['ezafe_kari'] != '':
                    ezafe_kari = data['ezafe_kari']
                    ezafe_kari = ezafe_kari.split(':')
                    ezafe_kari = round((int(ezafe_kari[0]) + (int(ezafe_kari[1]) / 60)), 6)
                    data['ezafe_kari'] = ezafe_kari
                elif data['ezafe_kari'] == '':
                    data['ezafe_kari'] = 0
            except:
                self.validate_status = False
                self.error_messages.append('برای اضافه کاری یک ساعت صحیح وارد کنید')

            try:
                if ':' not in data['tatil_kari']:
                    data['tatil_kari'] = int(data['tatil_kari'])
                elif data['tatil_kari'] and data['tatil_kari'] != '':
                    tatil_kari = data['tatil_kari']
                    tatil_kari = tatil_kari.split(':')
                    tatil_kari = round((int(tatil_kari[0]) + (int(tatil_kari[1]) / 60)), 6)
                    data['tatil_kari'] = tatil_kari
                elif data['tatil_kari'] == '':
                    data['tatil_kari'] = 0
            except:
                self.validate_status = False
                self.error_messages.append('برای تعطیل کاری یک ساعت صحیح وارد کنید')

            try:
                if ':' not in data['kasre_kar']:
                    data['kasre_kar'] = int(data['kasre_kar'])
                elif data['kasre_kar'] and data['kasre_kar'] != '':
                    kasre_kar = data['kasre_kar']
                    kasre_kar = kasre_kar.split(':')
                    kasre_kar = round((int(kasre_kar[0]) + (int(kasre_kar[1]) / 60)), 6)
                    data['kasre_kar'] = kasre_kar
                elif data['kasre_kar'] == '':
                    data['kasre_kar'] = 0
            except:
                self.validate_status = False
                self.error_messages.append('برای کسر کار یک ساعت صحیح وارد کنید')

            try:
                if ':' not in data['shab_kari']:
                    data['shab_kari'] = int(data['shab_kari'])
                elif data['shab_kari'] and data['shab_kari'] != '':
                    shab_kari = data['shab_kari']
                    shab_kari = shab_kari.split(':')
                    shab_kari = round((int(shab_kari[0]) + (int(shab_kari[1]) / 60)), 6)
                    data['shab_kari'] = shab_kari
                elif data['shab_kari'] == '':
                    data['shab_kari'] = 0
            except:
                self.validate_status = False
                self.error_messages.append('برای شب کاری یک ساعت صحیح وارد کنید')

            if self.validate_status:
                serializer = ListOfPayItemsAddInfoSerializer(query, data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                counter = 1
                response = []
                for error in self.error_messages:
                    error = str(counter) + '-' + error
                    counter += 1
                    response.append(error)
                return Response({'وضعیت': response}, status=status.HTTP_400_BAD_REQUEST)
        else:
            query.delete()
            return Response({'status': 'deleted'}, status=status.HTTP_200_OK)


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
        new_list_of_pay.ultimate = False
        new_list_of_pay.use_in_calculate = data['use_in_calculate']
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
            new_item.entitlement_leave_day = 0
            new_item.matter_47_leave_day = 0
            new_item.daily_entitlement_leave_day = 0
            new_item.hourly_entitlement_leave_day = 0
            new_item.absence_day = 0
            new_item.illness_leave_day = 0
            new_item.without_salary_leave_day = 0
            new_item.mission_day = 0

            new_item.save()
        return Response({'id': list_of_pay.id}, status=status.HTTP_201_CREATED)


class ListOfPayUltimateApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'

    def __init__(self):
        self.validate_status = True
        self.response_message = ''

    def post(self, request, pk):
        ultimate = request.data['ultimate']
        list_of_pay = ListOfPay.objects.get(pk=pk)
        same_lists = ListOfPay.objects.filter(Q(year=list_of_pay.year) & Q(month=list_of_pay.month)
                                              & Q(workshop=list_of_pay.workshop))
        if ultimate:
            if len(list_of_pay.list_of_pay_item.all()) == 0:
                self.validate_status = False
                self.response_message = 'در این لیست پرسنلی موجود نیست'
                response = list_of_pay.info_for_items
            for item in list_of_pay.list_of_pay_item.all():
                if item.sanavat_notice:
                    self.validate_status = False
                    self.response_message = 'یکی از پرسنل مشمول پایه سنوات شده است لطفا حکم جدید صادر کنید'

            if list_of_pay.use_in_calculate:
                for same_list in same_lists:
                    if same_list.use_in_calculate and same_list.ultimate:
                        self.validate_status = False
                        self.response_message = 'ابتدا تمام لیست های با بیمه و مالیات این ماه را غیر نهایی کنید'
            elif not list_of_pay.use_in_calculate:
                for same_list in same_lists:
                    if not same_list.use_in_calculate and same_list.ultimate:
                        self.validate_status = False
                        self.response_message = 'ابتدا تمام لیست های بدون بیمه و مالیات این ماه را غیر نهایی کنید'
            if not list_of_pay.workshop.is_verified:
                self.validate_status = False
                self.response_message = 'ابتدا کارگاه این لیست را نهایی کنید'

            if self.validate_status:
                list_of_pay.ultimate = ultimate
                list_of_pay.save()
                return Response({'وضعیت': 'نهایی  کردن لیست حقوق انجام شد'}, status=status.HTTP_200_OK)
            else:
                return Response({'وضعیت': self.response_message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            list_of_pay.ultimate = False
            list_of_pay.save()
            return Response({'وضعیت': 'غیر نهایی  کردن لیست حقوق انجام شد'}, status=status.HTTP_200_OK)


class ListOfPayEditDetail(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay'

    def get_object(self, pk):
        try:
            return ListOfPay.objects.get(pk=pk)
        except ListOfPay.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ListOfPayEditSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        serializer = ListOfPayEditSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cumulative = {}
            for item in query.list_of_pay_item.all():
                cumulative[item.workshop_personnel.id] = {
                    'cumulative_absence': item.cumulative_absence,
                    'cumulative_mission': item.cumulative_mission,
                    'cumulative_entitlement': item.cumulative_entitlement,
                    'cumulative_illness': item.cumulative_illness,
                    'cumulative_without_salary': item.cumulative_without_salary,
                    'ezafe_kari': item.ezafe_kari,
                    'tatil_kari': item.tatil_kari,
                    'kasre_kar': item.kasre_kar,
                    'sayer_kosoorat': item.sayer_kosoorat,
                    'shab_kari': item.shab_kari,
                    'nobat_kari_sob_asr': item.nobat_kari_sob_asr,
                    'nobat_kari_sob_shab': item.nobat_kari_sob_shab,
                    'nobat_kari_asr_shab': item.nobat_kari_asr_shab,
                    'nobat_kari_sob_asr_shab': item.nobat_kari_sob_asr_shab,
                    'sayer_ezafat': item.sayer_ezafat,
                    'contract_row': item.contract_row,
                    'mazaya_gheyr_mostamar': item.mazaya_gheyr_mostamar,
                    'hazine_made_137': item.hazine_made_137,
                    'kosoorat_insurance': item.kosoorat_insurance,
                    'sayer_moafiat': item.sayer_moafiat,
                    'manategh_tejari_moafiat': item.manategh_tejari_moafiat,
                    'ejtenab_maliat_mozaaf': item.ejtenab_maliat_mozaaf,
                }
                item.delete()
            response = query.info_for_items
            for item in response:
                workshop_personnel = WorkshopPersonnel.objects.filter(
                        Q(workshop=query.workshop) & Q(personnel_id=item['pk'])).first()
                try:
                    print(cumulative[workshop_personnel.id])
                except:
                    cumulative[workshop_personnel.id] = {
                        'cumulative_absence': 0,
                        'cumulative_mission': 0,
                        'cumulative_entitlement': 0,
                        'cumulative_illness': 0,
                        'cumulative_without_salary': 0,
                        'ezafe_kari': 0,
                        'tatil_kari': 0,
                        'kasre_kar': 0,
                        'sayer_kosoorat': 0,
                        'shab_kari': 0,
                        'nobat_kari_sob_asr': 0,
                        'nobat_kari_sob_shab': 0,
                        'nobat_kari_asr_shab': 0,
                        'nobat_kari_sob_asr_shab': 0,
                        'sayer_ezafat': 0,
                        'contract_row': None,
                        'mazaya_gheyr_mostamar': 0,
                        'hazine_made_137': 0,
                        'kosoorat_insurance': 0,
                        'sayer_moafiat': 0,
                        'manategh_tejari_moafiat': 0,
                        'ejtenab_maliat_mozaaf': 0,

                    }

                if item['insurance']:
                    insurance = 'y'
                else:
                    insurance = 'n'

                payroll_list_item = ListOfPayItem.objects.create(
                    list_of_pay=query,
                    workshop_personnel=workshop_personnel,
                    contract=Contract.objects.get(pk=item['contract']),
                    normal_worktime=item['normal_work'],
                    real_worktime=item['real_work'],
                    mission_day=item['mission'],
                    is_insurance=insurance,
                    absence_day=item['leaves']['a'],
                    entitlement_leave_day=item['leaves']['e'],
                    daily_entitlement_leave_day=item['leaves']['ed'],
                    hourly_entitlement_leave_day=item['leaves']['eh'],
                    illness_leave_day=item['leaves']['i'] + item['leaves']['c'],
                    without_salary_leave_day=item['leaves']['w'],
                    matter_47_leave_day=item['leaves']['m'],
                    cumulative_absence=cumulative[workshop_personnel.id]['cumulative_absence'],
                    cumulative_mission=cumulative[workshop_personnel.id]['cumulative_mission'],
                    cumulative_entitlement=cumulative[workshop_personnel.id]['cumulative_entitlement'],
                    cumulative_illness=cumulative[workshop_personnel.id]['cumulative_illness'],
                    cumulative_without_salary=cumulative[workshop_personnel.id]['cumulative_without_salary'],
                    ezafe_kari=cumulative[workshop_personnel.id]['ezafe_kari'],
                    tatil_kari=cumulative[workshop_personnel.id]['tatil_kari'],
                    kasre_kar=cumulative[workshop_personnel.id]['kasre_kar'],
                    sayer_kosoorat=cumulative[workshop_personnel.id]['sayer_kosoorat'],
                    shab_kari=cumulative[workshop_personnel.id]['shab_kari'],
                    nobat_kari_sob_asr=cumulative[workshop_personnel.id]['nobat_kari_sob_asr'],
                    nobat_kari_sob_shab=cumulative[workshop_personnel.id]['nobat_kari_sob_shab'],
                    nobat_kari_asr_shab=cumulative[workshop_personnel.id]['nobat_kari_asr_shab'],
                    nobat_kari_sob_asr_shab=cumulative[workshop_personnel.id]['nobat_kari_sob_asr_shab'],
                    sayer_ezafat=cumulative[workshop_personnel.id]['sayer_ezafat'],
                    contract_row=cumulative[workshop_personnel.id]['contract_row'],
                    mazaya_gheyr_mostamar=cumulative[workshop_personnel.id]['mazaya_gheyr_mostamar'],
                    hazine_made_137=cumulative[workshop_personnel.id]['hazine_made_137'],
                    kosoorat_insurance=cumulative[workshop_personnel.id]['kosoorat_insurance'],
                    sayer_moafiat=cumulative[workshop_personnel.id]['sayer_moafiat'],
                    manategh_tejari_moafiat=cumulative[workshop_personnel.id]['manategh_tejari_moafiat'],
                    ejtenab_maliat_mozaaf=cumulative[workshop_personnel.id]['ejtenab_maliat_mozaaf'],
                )
                payroll_list_item.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOfPayEditItems(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'list_of_pay_item'

    def get_object(self, pk):
        try:
            return ListOfPayItem.objects.filter(list_of_pay=pk)
        except ListOfPayItem.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ListOfPayItemsAddInfoSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ContractEditApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ContractEditSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        data = request.data
        list_of_pays = query.list_of_pay_item.all()
        if data['quit_job_date']:
            quit_job_month = int(data['quit_job_date'].split('-')[1])
            for item in list_of_pays:
                if item.list_of_pay.month >= quit_job_month:
                    raise ValidationError('در این تاریخ ترک کار، لیست حقوق صادر شده')
        serializer = ContractEditSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractInsuranceEditApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ContractEditInsuranceSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        data = request.data
        list_of_pays = query.list_of_pay_item.all()
        if data['insurance']:
            if not data['insurance_add_date']:
                raise ValidationError(' تاریخ اضافه شدن به لیست بیمه را وارد کنید')
            if data['insurance_add_date']:
                insurance_add_date = int(data['insurance_add_date'].split('-')[1])
                for item in list_of_pays:
                    if item.list_of_pay.month >= insurance_add_date:
                        raise ValidationError('در این تاریخ اضافه شدن به لیست بیمه، لیست حقوق صادر شده')
            if data['insurance_number']:
                if len(data['insurance_number']) != 10:
                    raise ValidationError('طول شماره بیمه باید 10 رقم باشد')
                elif data['insurance_number'][:2] != '00':
                    raise ValidationError(' شماره بیمه باید با 00 شروع شود')
            elif not data['insurance_number']:
                raise ValidationError(' شماره بیمه را وارد کنید')

        serializer = ContractEditInsuranceSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractTaxEditApi(APIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_basename = 'contract'

    def get_object(self, pk):
        try:
            return Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ContractEditTaxSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = self.get_object(pk)
        data = request.data
        list_of_pays = query.list_of_pay_item.all()
        if data['tax'] and not data['tax_add_date']:
            raise ValidationError(' تاریخ اضافه شدن به لیست مالیات را وارد کنید')
        if data['tax_add_date']:
            tax_add_date = int(data['tax_add_date'].split('-')[1])
            for item in list_of_pays:
                if item.list_of_pay.month >= tax_add_date:
                    raise ValidationError('در این تاریخ اضافه شدن به لیست مالیات، لیست حقوق صادر شده')
        serializer = ContractEditTaxSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
