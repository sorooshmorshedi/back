import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from helpers.filters import BASE_FIELD_FILTERS
from payroll.models import Workshop, Personnel, PersonnelFamily, WorkshopPersonnel, ContractRow, ContractTime


class WorkshopFilter(filters.FilterSet):
    class Meta:
        model = Workshop
        fields = {
            'id': ('exact',),
            'company': ('exact',),
            'code': BASE_FIELD_FILTERS,
            'name': BASE_FIELD_FILTERS,
            'employer_name': BASE_FIELD_FILTERS,
            'address': ['icontains'],
            'employer_insurance_contribution': ('exact',),
            'branch_code': ('exact',),
            'branch_name': BASE_FIELD_FILTERS,
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
            'personnel_code': ('exact',),
            'gender': ('exact',),
            'military_service': ('exact',),
            'national_code': ('exact',),
            'identity_code': ('exact',),
            'date_of_birth': BASE_FIELD_FILTERS,
            'date_of_exportation': BASE_FIELD_FILTERS,
            'location_of_birth': BASE_FIELD_FILTERS,
            'location_of_exportation': BASE_FIELD_FILTERS,
            'sector_of_exportation': BASE_FIELD_FILTERS,
            'marital_status': ('exact',),
            'number_of_childes': ('exact',),
            'city_phone_code': ('exact',),
            'phone_number': ('exact',),
            'mobile_number_1': ('exact',),
            'mobile_number_2': ('exact',),
            'address': BASE_FIELD_FILTERS,
            'postal_code': BASE_FIELD_FILTERS,
            'insurance': BASE_FIELD_FILTERS,
            'insurance_code': BASE_FIELD_FILTERS,
            'degree_of_education': ('exact',),
            'field_of_study':  BASE_FIELD_FILTERS,
            'university_type': ('exact',),
            'university_name': ('exact',),
            'account_bank_name': BASE_FIELD_FILTERS,
            'account_bank_number': ('exact',),
            'sheba_number': ('exact',),
            'is_personnel_active': BASE_FIELD_FILTERS,

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class PersonnelFamilyFilter(filters.FilterSet):
    class Meta:
        model = PersonnelFamily
        fields = {
            'id': ('exact',),
            'personnel': ('exact',),
            'name': BASE_FIELD_FILTERS,
            'last_name': BASE_FIELD_FILTERS,
            'national_code': ('exact',),
            'date_of_birth': BASE_FIELD_FILTERS,
            'relative': ('exact',),
            'marital_status': ('exact',),
            'military_service': ('exact',),
            'study_status': ('exact',),
            'physical_condition': ('exact',),
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class WorkshopPersonnelFilter(filters.FilterSet):
    class Meta:
        model = WorkshopPersonnel
        fields = {
            'id': ('exact',),
            'personnel': ('exact',),
            'workshop': ('exact',),
            'insurance': BASE_FIELD_FILTERS,
            'insurance_add_date': BASE_FIELD_FILTERS,
            'work_title': ['icontains'],
            'previous_insurance_history_out_workshop': ('exact',),
            'previous_insurance_history_in_workshop': ('exact',),
            'current_insurance_history_in_workshop': ('exact',),
            'insurance_history_totality': ('exact',),
            'job_position': BASE_FIELD_FILTERS,
            'job_group': BASE_FIELD_FILTERS,
            'job_location': BASE_FIELD_FILTERS,
            'job_location_status': BASE_FIELD_FILTERS,
            'employment_type': ('exact',),
            'contract_type': ('exact',),
            'employee_status': ('exact',),

        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ContractRowFilter(filters.FilterSet):
    class Meta:
        model = ContractRow
        fields = {
            'id': ('exact',),
            'workshop': ('exact',),
            'contract_row': ('exact',),
            'contract_number': ('exact',),
            'registration_date': BASE_FIELD_FILTERS,
            'from_date': BASE_FIELD_FILTERS,
            'to_date': BASE_FIELD_FILTERS,
            'is_activate': BASE_FIELD_FILTERS,
            'assignor_name': BASE_FIELD_FILTERS,
            'assignor_national_code': ('exact',),
            'assignor_workshop_code': ('exact',),
            'contract_initial_amount': BASE_FIELD_FILTERS,
            'branch': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class ContractTimeFilter(filters.FilterSet):
    class Meta:
        model = ContractTime
        fields = {
            'id': ('exact',),
            'workshop_personnel': ('exact',),
            'code': ('exact',),
            'contract_from_date': BASE_FIELD_FILTERS,
            'contract_to_date': BASE_FIELD_FILTERS,
            'quit_job_date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }
