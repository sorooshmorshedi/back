import django_filters
from django.db.models import Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from helpers.filters import BASE_FIELD_FILTERS
from payroll.models import Workshop, Personnel, PersonnelFamily, WorkshopPersonnel, ContractRow, Contract, \
    LeaveOrAbsence, Mission, HRLetter, WorkshopTaxRow, WorkshopTax, ListOfPay, ListOfPayItem, Loan, OptionalDeduction, \
    LoanItem, Adjustment


class WorkshopFilter(filters.FilterSet):
    class Meta:
        model = Workshop
        fields = {
            'id': ('exact',),
            'company': ('exact',),
            'code': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'employer_name': BASE_FIELD_FILTERS,
            'address': BASE_FIELD_FILTERS,
            'employer_insurance_contribution': BASE_FIELD_FILTERS,
            'postal_code': BASE_FIELD_FILTERS,
            'branch_code': BASE_FIELD_FILTERS,
            'branch_name': BASE_FIELD_FILTERS,
            'is_active': BASE_FIELD_FILTERS,
            'is_default': BASE_FIELD_FILTERS,
            'is_verified': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class PersonnelFilter(filters.FilterSet):
    class Meta:
        model = Personnel
        fields = {
            'id': ('exact',),
            'company': ('exact',),
            'name': BASE_FIELD_FILTERS,
            'last_name': BASE_FIELD_FILTERS,
            'father_name': BASE_FIELD_FILTERS,
            'country': BASE_FIELD_FILTERS,
            'nationality': ('exact',),
            'personnel_code': BASE_FIELD_FILTERS,
            'gender': ('exact',),
            'military_service': ('exact',),
            'national_code': BASE_FIELD_FILTERS,
            'identity_code': BASE_FIELD_FILTERS,
            'date_of_birth': BASE_FIELD_FILTERS,
            'date_of_exportation': BASE_FIELD_FILTERS,
            'location_of_birth': BASE_FIELD_FILTERS,
            'location_of_exportation': BASE_FIELD_FILTERS,
            'sector_of_exportation': BASE_FIELD_FILTERS,
            'marital_status': ('exact',),
            'number_of_childes': ('exact',),
            'city_phone_code': BASE_FIELD_FILTERS,
            'phone_number': BASE_FIELD_FILTERS,
            'mobile_number_1': BASE_FIELD_FILTERS,
            'mobile_number_2': BASE_FIELD_FILTERS,
            'address': BASE_FIELD_FILTERS,
            'postal_code': BASE_FIELD_FILTERS,
            'insurance': BASE_FIELD_FILTERS,
            'insurance_code': BASE_FIELD_FILTERS,
            'degree_education': ('exact',),
            'field_of_study': BASE_FIELD_FILTERS,
            'university_type': ('exact',),
            'university_name': BASE_FIELD_FILTERS,
            'account_bank_name': ('exact',),
            'account_bank_number': BASE_FIELD_FILTERS,
            'bank_cart_number': BASE_FIELD_FILTERS,
            'sheba_number': BASE_FIELD_FILTERS,
            'is_personnel_active': ('exact',),
            'is_personnel_verified': ('exact',),

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


def personnel_filter(queryset, name, value):
    query = []
    for item in queryset:
        if item.personnel and value in item.personnel.full_name:
            query.append(item.id)
    return queryset.filter(id__in=query)


class PersonnelFamilyFilter(filters.FilterSet):
    personnel_name = filters.CharFilter(method=personnel_filter)

    class Meta:
        model = PersonnelFamily
        fields = {
            'id': ('exact',),
            'personnel': ('exact',),
            'name': BASE_FIELD_FILTERS,
            'last_name': BASE_FIELD_FILTERS,
            'national_code': BASE_FIELD_FILTERS,
            'date_of_birth': BASE_FIELD_FILTERS,
            'relative': ('exact',),
            'marital_status': ('exact',),
            'military_service': ('exact',),
            'study_status': ('exact',),
            'physical_condition': ('exact',),
            'is_active': ('exact',),
            'is_verified': ('exact',),
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


def workshop_filter(queryset, name, value):
    query = []
    for item in queryset:
        if item.workshop and value in item.workshop.workshop_title:
            query.append(item.id)
    return queryset.filter(id__in=query)


def employment_type_filter(queryset, name, value):
    types = {
        'پیمانی': 4,
        'قراردادی': 1,
        'َشرکتی': 2,
        'مامور': 5,
        'رسمی': 3,
        'سایر': 6,
    }
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(employment_type=types[type])
    return query

def job_group_filter(queryset, name, value):
    types = {}
    for item in WorkshopPersonnel.JOB_GROUP_TYPES:
        types[item[1]] = item[0]
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(job_group=types[type])
    return query

def contract_type_filter(queryset, name, value):
    types = {}
    for item in WorkshopPersonnel.CONTRACT_TYPES:
        types[item[1]] = item[0]
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(contract_type=types[type])
    return query

def employee_status_filter(queryset, name, value):
    types = {}
    for item in WorkshopPersonnel.EMPLOYEE_TYPES:
        types[item[1]] = item[0]
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(employee_status=types[type])
    return query


class WorkshopPersonnelFilter(filters.FilterSet):

    personnel_name = filters.CharFilter(method=personnel_filter)
    workshop_name = filters.CharFilter(method=workshop_filter)
    employment_type_display = filters.CharFilter(method=employment_type_filter)
    job_group_display = filters.CharFilter(method=job_group_filter)
    contract_type_display = filters.CharFilter(method=contract_type_filter)
    employee_status_display = filters.CharFilter(method=employee_status_filter)

    class Meta:
        model = WorkshopPersonnel
        fields = {
            'id': ('exact',),
            'personnel': ('exact',),
            'workshop': ('exact',),
            'work_title': BASE_FIELD_FILTERS,
            'previous_insurance_history_out_workshop': BASE_FIELD_FILTERS,
            'previous_insurance_history_in_workshop': BASE_FIELD_FILTERS,
            'current_insurance_history_in_workshop': BASE_FIELD_FILTERS,
            'insurance_history_totality': BASE_FIELD_FILTERS,
            'job_position': BASE_FIELD_FILTERS,
            'job_group': BASE_FIELD_FILTERS,
            'job_location': BASE_FIELD_FILTERS,
            'job_location_status': BASE_FIELD_FILTERS,
            'employment_date': BASE_FIELD_FILTERS,
            'employment_type': ('exact',),
            'contract_type': ('exact',),
            'employee_status': ('exact',),
            'is_verified': BASE_FIELD_FILTERS,

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


def Workshop_personnel_filter(queryset, name, value):
    query = []
    for item in queryset:
        if item.workshop_personnel:
            if value in item.workshop_personnel.personnel.full_name:
                query.append(item.id)
            if value in item.workshop_personnel.workshop.name:
                query.append(item.id)
    return queryset.filter(id__in=query)


class ContractFilter(filters.FilterSet):
    workshop_personnel_display = filters.CharFilter(method=Workshop_personnel_filter)
    class Meta:
        model = Contract
        fields = {
            'id': ('exact',),
            'workshop_personnel': ('exact',),
            'code': BASE_FIELD_FILTERS,
            'insurance': BASE_FIELD_FILTERS,
            'insurance_add_date': BASE_FIELD_FILTERS,
            'contract_from_date': BASE_FIELD_FILTERS,
            'insurance_number': BASE_FIELD_FILTERS,
            'contract_to_date': BASE_FIELD_FILTERS,
            'quit_job_date': BASE_FIELD_FILTERS,
            'is_verified': ('exact',),

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ContractRowFilter(filters.FilterSet):
    workshop_name = filters.CharFilter(method=workshop_filter)

    class Meta:
        model = ContractRow
        fields = {
            'id': ('exact',),
            'workshop': ('exact',),
            'contract_row': BASE_FIELD_FILTERS,
            'contract_number': BASE_FIELD_FILTERS,
            'registration_date': BASE_FIELD_FILTERS,
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
            'assignor_name': BASE_FIELD_FILTERS,
            'assignor_national_code': BASE_FIELD_FILTERS,
            'assignor_workshop_code': BASE_FIELD_FILTERS,
            'contract_initial_amount': BASE_FIELD_FILTERS,
            'branch': BASE_FIELD_FILTERS,
            'status': ('exact',),
            'is_verified': ('exact',),
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class AdjustmentFilter(filters.FilterSet):
    class Meta:
        model = Adjustment
        fields = {
            'id': ('exact',),
            'contract_row': ('exact',),
            'date': BASE_FIELD_FILTERS,
            'change_date': BASE_FIELD_FILTERS,
            'amount': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


def absence_type_filter(queryset, name, value):
    types = {
        'استحقاقی': 'e',
        'استعلاجی': 'i',
        'بدون_حقوق': 'w',
        'غیبت': 'a',
        'ماده_73': 'm',
        'زایمان': 'c'
    }
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(leave_type=types[type])
    return query


class LeaveOrAbsenceFilter(filters.FilterSet):
    leave_type_display = filters.CharFilter(method=absence_type_filter)
    workshop_personnel_display = filters.CharFilter(method=Workshop_personnel_filter)

    class Meta:
        model = LeaveOrAbsence
        fields = {
            'id': BASE_FIELD_FILTERS,
            'workshop_personnel': ('exact',),
            'leave_type': ('exact',),
            'entitlement_leave_type': ('exact',),
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
            'from_hour': BASE_FIELD_FILTERS,
            'to_hour': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
            'is_verified': BASE_FIELD_FILTERS,

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


def mission_type_filter(queryset, name, value):
    types = {
        'ساعتی': 'h',
        'روزانه': 'd',
    }
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(mission_type=types[type])
    return query



class MissionFilter(filters.FilterSet):
    mission_type_display = filters.CharFilter(method=mission_type_filter)
    workshop_personnel_display = filters.CharFilter(method=Workshop_personnel_filter)

    class Meta:
        model = Mission
        fields = {
            'id': BASE_FIELD_FILTERS,
            'workshop_personnel': ('exact',),
            'mission_type': ('exact',),
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
            'is_verified': BASE_FIELD_FILTERS,

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


def is_template_filter(queryset, name, value):
    types = {
        'قالب': 't',
        'شخصی': 'p',
    }
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(is_template=types[type])
    return query


def contract_code_filter(queryset, name, value):
    query = []
    for item in queryset:
        if item.contract:
            if value in item.contract.code:
                query.append(item.id)
    return queryset.filter(id__in=query)


def contract_workshop_personnel_filter(queryset, name, value):
    query = []
    for item in queryset:
        if item.contract:
            if value in item.contract.workshop_personnel.personnel.full_name:
                query.append(item.id)
            if value in item.contract.workshop_personnel.workshop.name:
                query.append(item.id)
    return queryset.filter(id__in=query)


class HRLetterFilter(filters.FilterSet):
    is_template_display = filters.CharFilter(method=is_template_filter)
    contract_code = filters.CharFilter(method=contract_code_filter)
    contract_detail = filters.CharFilter(method=contract_workshop_personnel_filter)

    class Meta:
        model = HRLetter
        fields = {
            'id': BASE_FIELD_FILTERS,
            'contract': ('exact',),
            'name': BASE_FIELD_FILTERS,
            'is_template': BASE_FIELD_FILTERS,
            'is_calculated': BASE_FIELD_FILTERS,
            'is_verified': BASE_FIELD_FILTERS,
            'hoghooghe_roozane_amount': BASE_FIELD_FILTERS,
            'paye_sanavat_amount': BASE_FIELD_FILTERS,
            'haghe_maskan_amount': BASE_FIELD_FILTERS,
            'bon_kharo_bar_amount': BASE_FIELD_FILTERS,
            'is_active': ('exact',),
        }


def month_filter(queryset, name, value):
    types = {}
    months = {
        1: 'فروردین',
        2: 'اردیبهشت',
        3: 'خرداد',
        4: 'تیر',
        5: 'مرداد',
        6: 'شهریور',
        7: 'مهر',
        8: 'آبان',
        9: 'آذر',
        10: 'دی',
        11: 'بهمن',
        12: 'اسفند',
    }
    for item in months:
        types[months[item]] = item
    query = queryset.filter(pk=None)
    for type in types:
        if value in type:
            query = queryset.filter(month=types[type])
    return query


class ListOfPayFilter(filters.FilterSet):
    month_name = filters.CharFilter(method=month_filter)
    workshop_display = filters.CharFilter(method=workshop_filter)

    class Meta:
        model = ListOfPay
        fields = {
            'id': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'workshop': ('exact',),
            'year': BASE_FIELD_FILTERS,
            'month': BASE_FIELD_FILTERS,
            'ultimate': BASE_FIELD_FILTERS,
            'use_in_calculate': BASE_FIELD_FILTERS,
            'pay_done': BASE_FIELD_FILTERS,
            'pay_form_create_date': BASE_FIELD_FILTERS,
            'bank_pay_date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ListOfPayItemFilter(filters.FilterSet):
    class Meta:
        model = ListOfPayItem
        fields = {
            'id': BASE_FIELD_FILTERS,
            'list_of_pay': ('exact',),
            'workshop_personnel': ('exact',),
            'contract': ('exact',),
        }


class TaxRowFilter(filters.FilterSet):
    class Meta:
        model = WorkshopTaxRow
        fields = {
            'id': BASE_FIELD_FILTERS,
        }


class TaxMoafFilter(filters.FilterSet):
    class Meta:
        model = WorkshopTax
        fields = {
            'id': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class LoanFilter(filters.FilterSet):
    workshop_personnel_display = filters.CharFilter(method=Workshop_personnel_filter)
    class Meta:
        model = Loan
        fields = {
            'id': BASE_FIELD_FILTERS,
            'workshop_personnel': ('exact',),
            'amount': BASE_FIELD_FILTERS,
            'pay_done': BASE_FIELD_FILTERS,
            'episode': ('exact',),
            'loan_type': ('exact',),
            'pay_date': BASE_FIELD_FILTERS,
            'is_verified': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class LoanItemFilter(filters.FilterSet):
    class Meta:
        model = LoanItem
        fields = {
            'id': BASE_FIELD_FILTERS,
            'loan': ('exact',),
            'amount': BASE_FIELD_FILTERS,
            'payed_amount': BASE_FIELD_FILTERS,
            'date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class DeductionFilter(filters.FilterSet):
    workshop_personnel_display = filters.CharFilter(method=Workshop_personnel_filter)
    class Meta:
        model = OptionalDeduction
        fields = {
            'id': BASE_FIELD_FILTERS,
            'workshop_personnel': ('exact',),
            'amount': BASE_FIELD_FILTERS,
            'pay_done': BASE_FIELD_FILTERS,
            'episode': ('exact',),
            'start_date': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'template_name': BASE_FIELD_FILTERS,
            'is_template': ('exact',),
            'is_verified': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class TaxFilter(filters.FilterSet):
    class Meta:
        model = ListOfPayItem
        fields = {
            'id': BASE_FIELD_FILTERS,
        }


class WorkshopTaxFilter(filters.FilterSet):
    class Meta:
        model = ListOfPay
        fields = {
            'id': BASE_FIELD_FILTERS,
        }


class TaxRowFilter(filters.FilterSet):
    class Meta:
        model = WorkshopTax
        fields = {
            'id': BASE_FIELD_FILTERS,
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }
