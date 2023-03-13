from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from helpers.auth import BasicCRUDPermission
from payroll.lists.filters import WorkshopFilter, PersonnelFilter, PersonnelFamilyFilter, WorkshopPersonnelFilter, \
    ContractRowFilter, LeaveOrAbsenceFilter, ContractFilter, MissionFilter, HRLetterFilter, TaxRowFilter, TaxFilter, \
    ListOfPayFilter, ListOfPayItemFilter, LoanFilter, DeductionFilter, LoanItemFilter, WorkshopTaxFilter, TaxMoafFilter, \
    AdjustmentFilter, PayFilter
from payroll.models import Workshop, Personnel, PersonnelFamily, WorkshopPersonnel, ContractRow, Contract, \
    LeaveOrAbsence, Mission, HRLetter, WorkshopTaxRow, WorkshopTax, ListOfPay, ListOfPayItem, Loan, OptionalDeduction, \
    LoanItem, Adjustment
from payroll.serializers import WorkShopSerializer, PersonnelSerializer, PersonnelFamilySerializer, \
    WorkshopPersonnelSerializer, ContractRowSerializer, LeaveOrAbsenceSerializer, ContractSerializer, MissionSerializer, \
    HRLetterSerializer, WorkshopTaxRowSerializer, WorkShopTaxSerializer, ListOfPaySerializer, ListOfPayItemSerializer, \
    LoanSerializer, DeductionSerializer, LoanItemSerializer, ListOfPayItemLessSerializer, ListOfPayLessSerializer, \
    ListOfPayInsuranceSerializer, ListOfPayItemInsuranceSerializer, PersonTaxSerializer, TaxSerializer, \
    AdjustmentSerializer, ListOfPayPaySerializer

from django.http import HttpResponse

import dbf

def write_insurance_diskette(request, pk):
    item = ListOfPay.objects.get(pk=pk)
    data = item.data_for_insurance

    new_table = dbf.Table('DSKKAR00.dbf',
                          'DSK_ID C(10); DSK_NAME C(100); DSK_FARM C(100); DSK_ADRS C(100); DSK_KIND N(1,0); DSK_YY N(2,0); DSK_MM N(2,0); DSK_LISTNO C(12); ; DSK_DISC C(100); DSK_NUM N(5,0);  DSK_TDD N(6,0);  DSK_TROOZ N(12,0);  DSK_TMAH N(12,0);  DSK_TMAZ N(12,0);  DSK_TMASH N(12,0);  DSK_TTOTL N(12,0);  DSK_TBIME N(12,0);  DSK_TKOSO N(12,0);  DSK_BIC N(12,0);  DSK_RATE N(5,0);  DSK_PRATE N(2,0);  DSK_BIMH N(12,0);  MON_PYM N(3,0)', codepage='utf8')
    new_table.open(dbf.READ_WRITE)
    new_table.append({
        'DSK_ID': data['DSK_ID'],
        'DSK_NAME': data['DSK_NAME'],
        'DSK_FARM': data['DSK_FARM'],
        'DSK_ADRS': data['DSK_ADRS'],
        'DSK_KIND': data['DSK_KIND'],
        'DSK_YY': data['DSK_YY'],
        'DSK_MM': data['DSK_MM'],
        'DSK_LISTNO': data['DSK_LISTNO'],
        'DSK_DISC': data['DSK_DISC'],
        'DSK_NUM': data['DSK_NUM'],
        'DSK_TDD': data['DSK_TDD'],
        'DSK_TROOZ': data['DSK_TROOZ'],
        'DSK_TMAH': data['DSK_TMAH'],
        'DSK_TMAZ': data['DSK_TMAZ'],
        'DSK_TMASH': data['DSK_TMASH'],
        'DSK_TTOTL': data['DSK_TTOTL'],
        'DSK_TBIME': data['DSK_TBIME'],
        'DSK_TKOSO': data['DSK_TKOSO'],
        'DSK_BIC': data['DSK_TBIC'],
        'DSK_RATE': data['DSK_RATE'],
        'DSK_PRATE': data['DSK_PRATE'],
        'DSK_BIMH': data['DSK_BIMH'],
        'MON_PYM': '000',

    })
    response = HttpResponse(new_table)
    response['Content-Disposition'] = 'attachment; filename={0}'.format('DSKKAR00.dbf')
    return response


def write_row_insurance_diskette(request, pk1, pk2):
    item = ListOfPay.objects.get(pk=pk1)
    contract_row = ContractRow.objects.get(pk=pk2)
    data = item.data_for_insurance_row(pk2)
    new_table = dbf.Table('DSKKAR00.dbf',
                          'DSK_ID C(10); DSK_NAME C(100); DSK_FARM C(100); DSK_ADRS C(100); DSK_KIND N(1,0); DSK_YY N(2,0); DSK_MM N(2,0); DSK_LISTNO C(12); ; DSK_DISC C(100); DSK_NUM N(5,0);  DSK_TDD N(6,0);  DSK_TROOZ N(12,0);  DSK_TMAH N(12,0);  DSK_TMAZ N(12,0);  DSK_TMASH N(12,0);  DSK_TTOTL N(12,0);  DSK_TBIME N(12,0);  DSK_TKOSO N(12,0);  DSK_BIC N(12,0);  DSK_RATE N(5,0);  DSK_PRATE N(2,0);  DSK_BIMH N(12,0);  MON_PYM N(3,0)', codepage='utf8')
    new_table.open(dbf.READ_WRITE)
    new_table.append({
        'DSK_ID': data['DSK_ID'],
        'DSK_NAME': data['DSK_NAME'],
        'DSK_FARM': data['DSK_FARM'],
        'DSK_ADRS': data['DSK_ADRS'],
        'DSK_KIND': data['DSK_KIND'],
        'DSK_YY': data['DSK_YY'],
        'DSK_MM': data['DSK_MM'],
        'DSK_LISTNO': data['DSK_LISTNO'],
        'DSK_DISC': data['DSK_DISC'],
        'DSK_NUM': data['DSK_NUM'],
        'DSK_TDD': data['DSK_TDD'],
        'DSK_TROOZ': data['DSK_TROOZ'],
        'DSK_TMAH': data['DSK_TMAH'],
        'DSK_TMAZ': data['DSK_TMAZ'],
        'DSK_TMASH': data['DSK_TMASH'],
        'DSK_TTOTL': data['DSK_TTOTL'],
        'DSK_TBIME': data['DSK_TBIME'],
        'DSK_TKOSO': data['DSK_TKOSO'],
        'DSK_BIC': data['DSK_TBIC'],
        'DSK_RATE': data['DSK_RATE'],
        'DSK_PRATE': data['DSK_PRATE'],
        'DSK_BIMH': data['DSK_BIMH'],
        'MON_PYM': contract_row.contract_row,

    })
    response = HttpResponse(new_table)
    response['Content-Disposition'] = 'attachment; filename={0}'.format('DSKKAR00.dbf')
    return response


def workshop_person_insurance_diskette(request, pk):
    items = ListOfPay.objects.get(pk=pk)
    new_table = dbf.Table('DSKWOR00.dbf',
                          'DSW_ID C(10); DSW_YY N(2,0); DSW_MM N(2,0); DSW_LISTNO C(12); DSW_ID1 C(10); DSW_FNAME C(100); DSW_LNAME C(100); DSW_DNAME C(100); DSW_IDNO C(15); DSW_IDPLC C(100); DSW_IDATE C(8); DSW_BDATE C(8); DSW_SEX C(3); DSW_NAT C(10);  DSW_OCP C(100);  DSW_SDATE C(8);  DSW_EDATE C(8);  DSW_DD N(2,0);  DSW_ROOZ N(12,0);  DSW_MAH N(12,0);  DSW_MAZ N(12,0);  DSW_MASH N(12,0);  DSW_TOTL N(12,0);  DSW_BIME N(12,0);  DSW_PRATE N(2,0);  DSW_JOB C(6); PER_NATCOD C(10)', codepage='utf8')
    new_table.open(dbf.READ_WRITE)
    for item in items.list_of_pay_item.all():
        if item.is_month_insurance:
            data = item.data_for_insurance
            new_table.append({
                'DSW_ID': data['DSW_ID'],
                'DSW_YY': data['DSW_YY'],
                'DSW_MM': data['DSW_MM'],
                'DSW_LISTNO': data['DSW_LISTNO'],
                'DSW_ID1': data['DSW_ID1'],
                'DSW_FNAME': data['DSW_FNAME'],
                'DSW_LNAME': data['DSW_LNAME'],
                'DSW_DNAME': data['DSW_DNAME'],
                'DSW_IDNO': data['DSW_IDNO'],
                'DSW_IDPLC': data['DSW_IDPLC'],
                'DSW_IDATE': data['DSW_IDATE'],
                'DSW_BDATE': data['DSW_BDATE'],
                'DSW_SEX': '',
                'DSW_NAT': '',
                'DSW_OCP': data['DSW_OCP'],
                'DSW_SDATE': data['DSW_SDATE'],
                'DSW_EDATE': data['DSW_EDATE'],
                'DSW_DD': data['DSW_DD'],
                'DSW_ROOZ': data['DSW_ROOZ'],
                'DSW_MAH': data['DSW_MAH'],
                'DSW_MAZ': data['DSW_MAZ'],
                'DSW_MASH': data['DSW_MASH'],
                'DSW_TOTL': data['DSW_TOTL'],
                'DSW_BIME': data['DSW_BIME'],
                'DSW_PRATE': data['DSW_PRATE'],
                'DSW_JOB': data['DSW_JOB'],
                'PER_NATCOD': data['PER_NATCOD'],

            })

    response = HttpResponse(new_table)
    response['Content-Disposition'] = 'attachment; filename={0}'.format('DSKWOR00.dbf')
    return response


def row_person_insurance_diskette(request, pk1, pk2):
    items = ListOfPay.objects.get(pk=pk1)
    new_table = dbf.Table('DSKWOR00.dbf',
                          'DSW_ID C(10); DSW_YY N(2,0); DSW_MM N(2,0); DSW_LISTNO C(12); DSW_ID1 C(10); DSW_FNAME C(100); DSW_LNAME C(100); DSW_DNAME C(100); DSW_IDNO C(15); DSW_IDPLC C(100); DSW_IDATE C(8); DSW_BDATE C(8); DSW_SEX C(3); DSW_NAT C(10);  DSW_OCP C(100);  DSW_SDATE C(8);  DSW_EDATE C(8);  DSW_DD N(2,0);  DSW_ROOZ N(12,0);  DSW_MAH N(12,0);  DSW_MAZ N(12,0);  DSW_MASH N(12,0);  DSW_TOTL N(12,0);  DSW_BIME N(12,0);  DSW_PRATE N(2,0);  DSW_JOB C(6); PER_NATCOD C(10)', codepage='utf8')
    new_table.open(dbf.READ_WRITE)

    for item in items.list_of_pay_item.filter(contract_row__id=pk2):
        if item.is_month_insurance:
            data = item.data_for_insurance
            new_table.append({
                'DSW_ID': data['DSW_ID'],
                'DSW_YY': data['DSW_YY'],
                'DSW_MM': data['DSW_MM'],
                'DSW_LISTNO': data['DSW_LISTNO'],
                'DSW_ID1': data['DSW_ID1'],
                'DSW_FNAME': data['DSW_FNAME'],
                'DSW_LNAME': data['DSW_LNAME'],
                'DSW_DNAME': data['DSW_DNAME'],
                'DSW_IDNO': data['DSW_IDNO'],
                'DSW_IDPLC': data['DSW_IDPLC'],
                'DSW_IDATE': data['DSW_IDATE'],
                'DSW_BDATE': data['DSW_BDATE'],
                'DSW_SEX': '',
                'DSW_NAT': '',
                'DSW_OCP': data['DSW_OCP'],
                'DSW_SDATE': data['DSW_SDATE'],
                'DSW_EDATE': data['DSW_EDATE'],
                'DSW_DD': data['DSW_DD'],
                'DSW_ROOZ': data['DSW_ROOZ'],
                'DSW_MAH': data['DSW_MAH'],
                'DSW_MAZ': data['DSW_MAZ'],
                'DSW_MASH': data['DSW_MASH'],
                'DSW_TOTL': data['DSW_TOTL'],
                'DSW_BIME': data['DSW_BIME'],
                'DSW_PRATE': data['DSW_PRATE'],
                'DSW_JOB': data['DSW_JOB'],
                'PER_NATCOD': data['PER_NATCOD'],

            })

        response = HttpResponse(new_table)
        response['Content-Disposition'] = 'attachment; filename={0}'.format('DSKWOR00.dbf')
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
        if item.is_month_tax:
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
            content += str(round(item.tax_naghdi_pension))
            content += ',0,1,0,1,0,'
            content += str(round(item.gheyre_naghdi_tax_pension))
            content += ','
            content += str(round(item.hazine_made_137))
            content += ','
            content += str(round(item.haghe_bime_moafiat))
            content += ',0,'
            content += str(round(item.total_sayer_moafiat))
            content += ','
            content += str(round(item.ezafe_kari_nakhales))
            content += ','
            content += str(round(item.tax_naghdi_un_pension))
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
            content += str(round(item.total_tax))
            content += '\n'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def write_summary_tax_diskette(request, pk):
    item = ListOfPay.objects.get(pk=pk)
    filename = "WK"
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
    content += str(workshop_personnel.title.code)
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


def write_new_persons_diskette(request, pks):
    workshop_personnels = WorkshopPersonnel.objects.filter(id__in=pks.split('-'))
    filename = "WP"
    filename += '.txt'
    content = ''
    print(workshop_personnels)
    for workshop_personnel in workshop_personnels:
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
        content += '\n'

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response



class WorkshopListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "getOwn.workshop"
    serializer_class = WorkShopSerializer
    filterset_class = WorkshopFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return Workshop.objects.hasAccess('get', self.permission_codename).filter(company=user.active_company)\
            .distinct('pk')


class PersonnelListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.personnel"
    serializer_class = PersonnelSerializer
    filterset_class = PersonnelFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return Personnel.objects.hasAccess('get', self.permission_codename).filter(company=user.active_company)\
            .distinct('pk')


class PersonnelFamilyListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.personnel_family"
    serializer_class = PersonnelFamilySerializer
    filterset_class = PersonnelFamilyFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return PersonnelFamily.objects.hasAccess('get', self.permission_codename)\
            .filter(personnel__company=user.active_company).distinct('pk')


class ContractListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.contract"
    serializer_class = ContractSerializer
    filterset_class = ContractFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        workhops_personnel, workhops_personnel_id = [], []
        for workshop in workhops:
            workhops_personnel.append(workshop.workshop_personnel.all())
        for workshop in workhops_personnel:
            for person in workshop:
                if person.id not in workhops_personnel_id:
                    workhops_personnel_id.append(person.id)
        return Contract.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop_personnel_id__in=workhops_personnel_id).distinct('pk')


class WorkshopPersonnelListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop_personnel"
    serializer_class = WorkshopPersonnelSerializer
    filterset_class = WorkshopPersonnelFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        return WorkshopPersonnel.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop__in=workhops).distinct('pk')


class ContractRowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.contract_row"
    serializer_class = ContractRowSerializer
    filterset_class = ContractRowFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        return ContractRow.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop__in=workhops).distinct('pk')


class AdjustmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.adjustment"
    serializer_class = AdjustmentSerializer
    filterset_class = AdjustmentFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        contracct_rows = ContractRow.objects.filter(workshop__in=workhops)
        return Adjustment.objects.hasAccess('get', self.permission_codename)\
            .filter(contract_row__in=contracct_rows).distinct('pk').reverse()


class LeaveOrAbsenceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.leave_or_absence"
    serializer_class = LeaveOrAbsenceSerializer
    filterset_class = LeaveOrAbsenceFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        workhops_personnel, workhops_personnel_id = [], []
        for workshop in workhops:
            workhops_personnel.append(workshop.workshop_personnel.all())
        for workshop in workhops_personnel:
            for person in workshop:
                if person.id not in workhops_personnel_id:
                    workhops_personnel_id.append(person.id)
        return LeaveOrAbsence.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop_personnel_id__in=workhops_personnel_id).distinct('pk')


class MissionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.mission"
    serializer_class = MissionSerializer
    filterset_class = MissionFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        workhops_personnel, workhops_personnel_id = [], []
        for workshop in workhops:
            workhops_personnel.append(workshop.workshop_personnel.all())
        for workshop in workhops_personnel:
            for person in workshop:
                if person.id not in workhops_personnel_id:
                    workhops_personnel_id.append(person.id)
        return Mission.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop_personnel_id__in=workhops_personnel_id).distinct('pk')


class HRLetterListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.hr_letter"
    serializer_class = HRLetterSerializer
    filterset_class = HRLetterFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return HRLetter.objects.hasAccess('get', self.permission_codename).filter(company=user.active_company)\
            .distinct('pk')

class ListOfPayListView(generics.ListAPIView):

    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.list_of_pay"
    serializer_class = ListOfPayLessSerializer
    filterset_class = ListOfPayFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        return ListOfPay.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop__in=workhops)


class ListOfPayInsuranceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.list_of_pay"
    serializer_class = ListOfPayInsuranceSerializer
    filterset_class = ListOfPayFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        return ListOfPay.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop__in=workhops)


class ListOfPayItemInsuranceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)
    permission_codename = "get.list_of_pay"
    serializer_class = ListOfPayItemInsuranceSerializer
    filterset_class = ListOfPayItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        items = []
        for workshop in workhops:
            for item in workshop.list_of_pay.all():
                items.append(item)
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename)\
            .filter(list_of_pay__in=items)


class ListOfPayItemLessListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay_item"
    serializer_class = ListOfPayItemSerializer
    filterset_class = ListOfPayItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        items = []
        for workshop in workhops:
            for item in workshop.list_of_pay.all():
                items.append(item)
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename)\
            .filter(list_of_pay__in=items)


class ListOfPayItemListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay_item"
    serializer_class = ListOfPayItemSerializer
    filterset_class = ListOfPayItemFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        items = []
        for workshop in workhops:
            for item in workshop.list_of_pay.all():
                items.append(item)
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename)\
            .filter(list_of_pay__in=items)


class TaxRowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop_tax_row"
    serializer_class = WorkshopTaxRowSerializer
    filterset_class = TaxRowFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        tax = company.tax.all()
        return WorkshopTaxRow.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop_tax__in=tax).distinct('pk')


class TaxMoafListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop_tax"
    serializer_class = WorkShopTaxSerializer
    filterset_class = TaxMoafFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return WorkshopTax.objects.hasAccess('get', self.permission_codename)\
            .filter(company=user.active_company).distinct('pk')


class LoanListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.loan"
    serializer_class = LoanSerializer
    filterset_class = LoanFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        workhops_personnel, workhops_personnel_id = [], []
        for workshop in workhops:
            workhops_personnel.append(workshop.workshop_personnel.all())
        for workshop in workhops_personnel:
            for person in workshop:
                if person.id not in workhops_personnel_id:
                    workhops_personnel_id.append(person.id)
        return Loan.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop_personnel_id__in=workhops_personnel_id).distinct('pk')


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
        user = self.request.user
        return OptionalDeduction.objects.hasAccess('get', self.permission_codename).filter(company=user.active_company)\
            .distinct('pk')


class PersonTaxListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay_item"
    serializer_class = PersonTaxSerializer
    filterset_class = TaxFilter
    ordering_fields = 'id', 'get_data_for_tax', 'data_for_tax', 'get_data_for_tax'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        items = []
        for workshop in workhops:
            for item in workshop.list_of_pay.all():
                items.append(item)
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename)\
            .filter(list_of_pay__in=items)


class TaxListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay"
    serializer_class = TaxSerializer
    filterset_class = WorkshopTaxFilter
    ordering_fields = 'id', 'data_for_tax', 'get_data_for_tax'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        items = []
        for workshop in workhops:
            for item in workshop.list_of_pay.all():
                items.append(item)
        return ListOfPayItem.objects.hasAccess('get', self.permission_codename)\
            .filter(list_of_pay__in=items)


class WorkshopAbsenceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop"
    serializer_class = WorkShopSerializer
    filterset_class = WorkshopFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return Workshop.objects.hasAccess('get', self.permission_codename)\
            .filter(company=user.active_company).distinct('pk')


class TaxRowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.workshop_tax"
    serializer_class = WorkShopTaxSerializer
    filterset_class = TaxRowFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        return WorkshopTax.objects.hasAccess('get', self.permission_codename)\
            .filter(company=company)


class PayListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, BasicCRUDPermission)

    permission_codename = "get.list_of_pay"
    serializer_class = ListOfPayPaySerializer
    filterset_class = PayFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        company = self.request.user.active_company
        workhops = company.workshop.all()
        return ListOfPay.objects.hasAccess('get', self.permission_codename)\
            .filter(workshop__in=workhops)
