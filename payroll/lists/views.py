from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from helpers.auth import BasicCRUDPermission
from payroll.lists.filters import WorkshopFilter, PersonnelFilter, PersonnelFamilyFilter, WorkshopPersonnelFilter, \
    ContractRowFilter, LeaveOrAbsenceFilter, ContractFilter, MissionFilter, HRLetterFilter, TaxRowFilter, TaxFilter, \
    ListOfPayFilter, ListOfPayItemFilter, LoanFilter, DeductionFilter, LoanItemFilter, WorkshopTaxFilter, TaxMoafFilter
from payroll.models import Workshop, Personnel, PersonnelFamily, WorkshopPersonnel, ContractRow, Contract, \
    LeaveOrAbsence, Mission, HRLetter, WorkshopTaxRow, WorkshopTax, ListOfPay, ListOfPayItem, Loan, OptionalDeduction, \
    LoanItem
from payroll.serializers import WorkShopSerializer, PersonnelSerializer, PersonnelFamilySerializer, \
    WorkshopPersonnelSerializer, ContractRowSerializer, LeaveOrAbsenceSerializer, ContractSerializer, MissionSerializer, \
    HRLetterSerializer, WorkshopTaxRowSerializer, WorkShopTaxSerializer, ListOfPaySerializer, ListOfPayItemSerializer, \
    LoanSerializer, DeductionSerializer, LoanItemSerializer, ListOfPayItemLessSerializer, ListOfPayLessSerializer, \
    ListOfPayInsuranceSerializer, ListOfPayItemInsuranceSerializer, PersonTaxSerializer, TaxSerializer

from django.http import HttpResponse

def write_insurance_diskette(request, pk):
    item = ListOfPay.objects.get(pk=pk)
    data = item.data_for_insurance
    filename = "DSKKAR.txt"
    content = ''
    content += str(data['DSK_ID'])
    content += ','
    content += str(data['DSK_NAME'])
    content += ','
    content += str(data['DSK_FARM'])
    content += ','
    content += str(data['DSK_ADRS'])
    content += ','
    content += str(data['DSK_KIND'])
    content += ','
    content += str(data['DSK_YY'])
    content += ','
    content += str(data['DSK_MM'])
    content += ','
    content += str(data['DSK_LISTNO'])
    content += ','
    content += str(data['DSK_DISC'])
    content += ','
    content += str(data['DSK_NUM'])
    content += ','
    content += str(data['DSK_TDD'])
    content += ','
    content += str(data['DSK_TROOZ'])
    content += ','
    content += str(data['DSK_TMAH'])
    content += ','
    content += str(data['DSK_TMAZ'])
    content += ','
    content += str(data['DSK_TMASH'])
    content += ','
    content += str(data['DSK_TTOTL'])
    content += ','
    content += str(data['DSK_TBIME'])
    content += ','
    content += str(data['DSK_TKOSO'])
    content += ','
    content += str(data['DSK_TBIC'])
    content += ','
    content += str(data['DSK_RATE'])
    content += ','
    content += str(data['DSK_PRATE'])
    content += ','
    content += str(data['DSK_BIMH'])
    content += ','
    content += str(data['DSK_PYM'])
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def write_person_insurance_diskette(request, pk):
    item = ListOfPayItem.objects.get(pk=pk)
    data = item.data_for_insurance
    filename = "DSKWOR.txt"
    content = ''
    content += str(data['DSW_ID'])
    content += ','
    content += str(data['DSW_YY'])
    content += ','
    content += str(data['DSW_MM'])
    content += ','
    content += str(data['DSW_LISTNO'])
    content += ','
    content += str(data['DSW_ID1'])
    content += ','
    content += str(data['DSW_FNAME'])
    content += ','
    content += str(data['DSW_LNAME'])
    content += ','
    content += str(data['DSW_DNAME'])
    content += ','
    content += str(data['DSW_IDNO'])
    content += ','
    content += str(data['DSW_IDPLC'])
    content += ','
    content += str(data['DSW_IDATE'])
    content += ','
    content += str(data['DSW_BDATE'])
    content += ','
    content += str(data['DSW_SEX'])
    content += ','
    content += str(data['DSW_NAT'])
    content += ','
    content += str(data['DSW_OCP'])
    content += ','
    content += str(data['DSW_SDATE'])
    content += ','
    content += str(data['DSW_EDATE'])
    content += ','
    content += str(data['DSW_DD'])
    content += ','
    content += str(round(data['DSW_ROOZ']))
    content += ','
    content += str(round(data['DSW_MAH']))
    content += ','
    content += str(round(data['DSW_MAZ']))
    content += ','
    content += str(round(data['DSW_MASH']))
    content += ','
    content += str(round(data['DSW_TOTL']))
    content += ','
    content += str(round(data['DSW_BIME']))
    content += ','
    content += str(data['DSW_PRATE'])
    content += ','
    content += str(data['DSW_JOB'])
    content += ','
    content += str(data['PER_NATCOD'])
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def write_tax_diskette(request, pk):
    item = ListOfPay.objects.get(pk=pk)
    items = item.list_of_pay_item.all()
    filename = "WH"
    filename += str(item.year)
    month = str(item.month)
    if len(month) < 2:
        month = ''.join(('0', month))
    filename += month
    filename += '.txt'
    content = ''
    for item in items:
        content += str(item.workshop_personnel.personnel.national_code)
        content += ',1,'
        content += str(item.year_real_work_month)
        content += ',0,85,1,'
        content += item.workshop_personnel.employment_date.__str__().replace('-', '')
        content += ',,'
        content += str(item.workshop_personnel.employee_status)
        content += ','
        content += str(item.workshop_personnel.job_location_status)
        content += ','
        content += str(round(item.naghdi_pension))
        content += ',0,1,0,1,0,'
        content += str(round(item.gheyre_naghdi_pension))
        content += ','
        content += str(round(item.hazine_made_137))
        content += ','
        content += str(round(item.haghe_bime_moafiat))
        content += ',0,'
        content += str(round(item.total_sayer_moafiat))
        content += ','
        content += str(round(item.ezafe_kari_nakhales))
        content += ','
        content += str(round(item.naghdi_un_pension))
        content += ',0,0,'
        content += str(round(item.mission_total))
        content += ','
        content += str(round(item.mazaya_gheyr_mostamar))
        content += ','
        content += str(round(item.get_padash))
        content += ','
        content += str(round(item.get_hagh_sanavat_and_save_leaves))
        content += ','
        content += str(round(item.get_hagh_sanavat_and_save_leaves))
        content += ',0,0,'
        content += str(round(item.calculate_month_tax))

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def write_summary_tax_diskette(request, pk):
    item = ListOfPay.objects.get(pk=pk)
    filename = "WH"
    filename += str(item.year)
    month = str(item.month)
    if len(month) < 2:
        month = ''.join(('0', month))
    filename += month
    filename += '.txt'

    content = ''
    content += str(item.year)
    content += ','
    content += str(item.month)
    content += ','
    content += str(round(item.month_tax))
    content += ',0,'
    content += str(item.sign_date[0])
    content += ',6,,,,,,,,'

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def write_new_person_diskette(request, pk):
    workshop_personnel = WorkshopPersonnel.objects.get(pk=pk)
    filename = "WP"
    filename += str(workshop_personnel.personnel.personnel_code)
    filename += '.txt'

    content = ''
    content += str(workshop_personnel.personnel.nationality)
    content += ','
    content += '1,'
    content += str(workshop_personnel.personnel.national_code)
    content += ','
    content += str(workshop_personnel.personnel.name)
    content += ','
    content += str(workshop_personnel.personnel.last_name)
    content += ','
    content += str(workshop_personnel.personnel.country)
    content += ','
    content += str(workshop_personnel.personnel.personnel_code)
    content += ','
    content += str(workshop_personnel.personnel.degree_education)
    content += ','
    content += str(workshop_personnel.work_title)
    content += ','
    content += str(workshop_personnel.personnel.insurance_for_tax)
    content += ',,'
    content += str(workshop_personnel.personnel.insurance_code)
    content += ','
    content += str(workshop_personnel.personnel.postal_code)
    content += ','
    content += str(workshop_personnel.personnel.address)
    content += ','
    content += str(workshop_personnel.employment_date)
    content += ','
    content += str(workshop_personnel.employment_type)
    content += ','
    content += str(workshop_personnel.job_location)
    content += ','
    content += str(workshop_personnel.job_location_status)
    content += ','
    content += str(workshop_personnel.contract_type)
    content += ',,'
    content += str(workshop_personnel.employee_status)
    content += ','
    content += str(workshop_personnel.personnel.mobile_number_1)
    content += ','

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response



class WorkshopListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop"
    serializer_class = WorkShopSerializer
    filterset_class = WorkshopFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Workshop.objects.hasAccess('get', self.permission_codename).all()


class PersonnelListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.personnel"
    serializer_class = PersonnelSerializer
    filterset_class = PersonnelFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Personnel.objects.hasAccess('get', self.permission_codename).all()


class PersonnelFamilyListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.personnel_family"
    serializer_class = PersonnelFamilySerializer
    filterset_class = PersonnelFamilyFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return PersonnelFamily.objects.hasAccess('get', self.permission_codename).all()


class SpecificPersonnelFamilyListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.personnel_family"
    serializer_class = PersonnelFamilySerializer
    filterset_class = PersonnelFamilyFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return PersonnelFamily.objects.hasAccess('get', self.permission_codename).filter()


class ContractListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.contract"
    serializer_class = ContractSerializer
    filterset_class = ContractFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Contract.objects.hasAccess('get', self.permission_codename).all()


class WorkshopPersonnelListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop_personnel"
    serializer_class = WorkshopPersonnelSerializer
    filterset_class = WorkshopPersonnelFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return WorkshopPersonnel.objects.hasAccess('get', self.permission_codename).all()


class ContractRowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.contract_row"
    serializer_class = ContractRowSerializer
    filterset_class = ContractRowFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ContractRow.objects.hasAccess('get', self.permission_codename).all()


class LeaveOrAbsenceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.leave_or_absence"
    serializer_class = LeaveOrAbsenceSerializer
    filterset_class = LeaveOrAbsenceFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return LeaveOrAbsence.objects.hasAccess('get', self.permission_codename).all()


class MissionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.mission"
    serializer_class = MissionSerializer
    filterset_class = MissionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Mission.objects.hasAccess('get', self.permission_codename).all()


class HRLetterListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.hr_letter"
    serializer_class = HRLetterSerializer
    filterset_class = HRLetterFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return HRLetter.objects.hasAccess('get', self.permission_codename).all()

class ListOfPayListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay"
    serializer_class = ListOfPayLessSerializer
    filterset_class = ListOfPayFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ListOfPay.objects.hasAccess('get', self.permission_codename).all().prefetch_related('list_of_pay_item')


class ListOfPayInsuranceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay"
    serializer_class = ListOfPayInsuranceSerializer
    filterset_class = ListOfPayFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ListOfPay.objects.hasAccess('get', self.permission_codename).all()

class ListOfPayItemInsuranceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay"
    serializer_class = ListOfPayItemInsuranceSerializer
    filterset_class = ListOfPayItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename).all()


class ListOfPayItemLessListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay_item"
    serializer_class = ListOfPayItemLessSerializer
    filterset_class = ListOfPayItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename).all()

class ListOfPayItemListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay_item"
    serializer_class = ListOfPayItemSerializer
    filterset_class = ListOfPayItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename).all()


class TaxRowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop_tax_row"
    serializer_class = WorkshopTaxRowSerializer
    filterset_class = TaxRowFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return WorkshopTaxRow.objects.hasAccess('get', self.permission_codename).all()


class TaxMoafListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop_tax"
    serializer_class = WorkShopTaxSerializer
    filterset_class = TaxMoafFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return WorkshopTax.objects.hasAccess('get', self.permission_codename).all()


class LoanListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.loan"
    serializer_class = LoanSerializer
    filterset_class = LoanFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Loan.objects.hasAccess('get', self.permission_codename).all()


class LoanItemListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.loan_item"
    serializer_class = LoanItemSerializer
    filterset_class = LoanItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return LoanItem.objects.hasAccess('get', self.permission_codename).all()


class DeductionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.deduction"
    serializer_class = DeductionSerializer
    filterset_class = DeductionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return OptionalDeduction.objects.hasAccess('get', self.permission_codename).all()


class PersonTaxListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay_item"
    serializer_class = PersonTaxSerializer
    filterset_class = TaxFilter
    ordering_fields = 'id', 'get_data_for_tax', 'data_for_tax', 'get_data_for_tax'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename).all()


class TaxListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay"
    serializer_class = TaxSerializer
    filterset_class = WorkshopTaxFilter
    ordering_fields = 'id', 'data_for_tax', 'get_data_for_tax'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ListOfPay.objects.hasAccess('get', self.permission_codename).all()


class WorkshopAbsenceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop"
    serializer_class = WorkShopSerializer
    filterset_class = WorkshopFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Workshop.objects.hasAccess('get', self.permission_codename).all()
