from payroll.models import Workshop, WorkshopPersonnel, Personnel, PersonnelFamily, ContractRow, HRLetter, Contract, \
    LeaveOrAbsence
from rest_framework import serializers


class WorkShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class PersonnelSerializer(serializers.ModelSerializer):
    nationality_display = serializers.CharField(source='get_nationality_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    military_service_display = serializers.CharField(source='get_military_service_display', read_only=True)
    marital_status_display = serializers.CharField(source='get_marital_status_display', read_only=True)
    degree_education_display = serializers.CharField(source='get_degree_education_display', read_only=True)
    university_type_display = serializers.CharField(source='get_university_type_display', read_only=True)

    class Meta:
        model = Personnel
        fields = '__all__'


class WorkshopPersonnelSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='personnel.name', read_only=True)
    personnel_last_name = serializers.CharField(source='personnel.last_name', read_only=True)
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    job_location_status_display = serializers.CharField(source='get_job_location_status_display', read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    contract_type_display = serializers.CharField(source='get_contract_type_display', read_only=True)
    employee_status_display = serializers.CharField(source='get_employee_status_display', read_only=True)
    job_position_display = serializers.CharField(source='get_job_position_display', read_only=True)


    class Meta:
        model = WorkshopPersonnel
        fields = '__all__'


class ContractRowSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ContractRow
        fields = '__all__'


class PersonnelFamilySerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='personnel.full_name', read_only=True)
    relative_display = serializers.CharField(source='get_relative_display', read_only=True)
    marital_status_display = serializers.CharField(source='get_marital_status_display', read_only=True)
    military_service_display = serializers.CharField(source='get_military_service_display', read_only=True)
    study_status_display = serializers.CharField(source='get_study_status_display', read_only=True)
    physical_condition_display = serializers.CharField(source='get_physical_condition_display', read_only=True)
    class Meta:
        model = PersonnelFamily
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.name', read_only=True)
    personnel_last_name = serializers.CharField(source='workshop_personnel.personnel.last_name', read_only=True)
    workshop_name = serializers.CharField(source='workshop_personnel.workshop.name', read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class HRLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = HRLetter
        fields = '__all__'


class LeaveOrAbsenceSerializer(serializers.ModelSerializer):
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)

    class Meta:
        model = LeaveOrAbsence
        fields = '__all__'


