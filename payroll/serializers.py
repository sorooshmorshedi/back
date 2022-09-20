from payroll.models import Workshop, WorkshopPersonnel, Personnel, PersonnelFamily, ContractRow, HRLetter, Contract, \
    LeaveOrAbsence, Mission, ListOfPay, ListOfPayItem, WorkshopTaxRow, WorkshopTax
from rest_framework import serializers


class WorkShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class WorkShopTaxRowsSerializer(serializers.ModelSerializer):
    from_amount_month = serializers.IntegerField(source='monthly_from_amount', read_only=True)
    to_amount_month = serializers.IntegerField(source='monthly_to_amount', read_only=True)
    auto_from = serializers.IntegerField(source='auto_from_amount', read_only=True)
    class Meta:
        model = WorkshopTaxRow
        fields = '__all__'


class WorkShopTaxSerializer(serializers.ModelSerializer):
    tax_row = WorkShopTaxRowsSerializer(many=True, read_only=True)
    class Meta:
        model = WorkshopTax
        fields = '__all__'


class WorkShopSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = 'id',  'base_pay_type', 'ezafe_kari_pay_type', 'tatil_kari_pay_type', 'kasre_kar_pay_type',\
                 'shab_kari_pay_type', 'aele_mandi_pay_type', 'nobat_kari_sob_asr_pay_type', 'mission_pay_type', \
                 'nobat_kari_sob_shab_pay_type', 'nobat_kari_asr_shab_pay_type', 'nobat_kari_sob_asr_shab_pay_type',\
                 'sanavat_type', 'ezafe_kari_nerkh', 'tatil_kari_nerkh', 'kasre_kar_nerkh', 'shab_kari_nerkh',\
                 'aele_mandi_nerkh', 'nobat_kari_sob_asr_nerkh', 'nobat_kari_sob_shab_nerkh',\
                 'nobat_kari_asr_shab_nerkh', 'nobat_kari_sob_asr_shab_nerkh', 'mission_pay_nerkh',\
                 'worker_insurance_nerkh', 'employee_insurance_nerkh', 'made_86', 'hade_aksar_mashmool_bime',\
                 'moafial_maliat_haghe_bime_sahme_bime_shavande', 'unemployed_insurance_nerkh',




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
    personnel_name = serializers.CharField(source='personnel.full_name', read_only=True)
    personnel_last_name = serializers.CharField(source='personnel.last_name', read_only=True)
    personnel_identity_code = serializers.CharField(source='personnel.identity_code', read_only=True)
    workshop_name = serializers.CharField(source='workshop.workshop_title', read_only=True)
    job_location_status_display = serializers.CharField(source='get_job_location_status_display', read_only=True)
    marital_display = serializers.CharField(source='personnel.get_marital_status_display', read_only=True)
    gender_display = serializers.CharField(source='personnel.get_gender_display', read_only=True)
    mobile_number = serializers.CharField(source='personnel.mobile_number_1', read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    contract_type_display = serializers.CharField(source='get_contract_type_display', read_only=True)
    employee_status_display = serializers.CharField(source='get_employee_status_display', read_only=True)
    job_group_display = serializers.CharField(source='get_job_group_display', read_only=True)

    class Meta:
        model = WorkshopPersonnel
        fields = '__all__'


class ContractRowSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    workshop_name = serializers.CharField(source='workshop.workshop_title', read_only=True)
    name = serializers.CharField(source='title', read_only=True)

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
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)
    personnel_last_name = serializers.CharField(source='workshop_personnel.personnel.last_name', read_only=True)
    workshop_name = serializers.CharField(source='workshop_personnel.workshop.name', read_only=True)
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class HRLetterSerializer(serializers.ModelSerializer):
    is_template_display = serializers.CharField(source='get_is_template_display', read_only=True)

    class Meta:
        model = HRLetter
        fields = '__all__'


class LeaveOrAbsenceSerializer(serializers.ModelSerializer):
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)

    class Meta:
        model = LeaveOrAbsence
        fields = '__all__'


class MissionSerializer(serializers.ModelSerializer):
    mission_type_display = serializers.CharField(source='get_mission_type_display', read_only=True)
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)

    class Meta:
        model = Mission
        fields = '__all__'


class ListOfPayItemSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)
    is_insurance_display = serializers.CharField(source='get_is_insurance_display', read_only=True)
    insurance_workshop = serializers.CharField(source='workshop_personnel.current_insurance_history_in_workshop',
                                               read_only=True)
    total_mission = serializers.IntegerField(source='mission_total', read_only=True)
    montly_pay = serializers.IntegerField(source='hoghoogh_mahane', read_only=True)
    sanavat_montly_pay = serializers.IntegerField(source='sanavat_mahane', read_only=True)
    contract_row_title = serializers.IntegerField(source='contract_row.contract_row', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = '__all__'


class ListOfPaySerializer(serializers.ModelSerializer):
    list_of_pay_item = ListOfPayItemSerializer(many=True)

    class Meta:
        model = ListOfPay
        fields = '__all__'


class WorkshopTaxRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopTaxRow
        fields = '__all__'


class ListOfPayItemsAddInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPayItem
        fields = 'id', 'ezafe_kari', 'tatil_kari', 'kasre_kar', 'shab_kari', 'nobat_kari_sob_asr', \
                 'nobat_kari_sob_shab', 'nobat_kari_asr_shab', 'nobat_kari_sob_asr_shab', 'sayer_ezafat', \
                 'list_of_pay', 'calculate_payment', 'contract_row'


class ListOfPayItemsKosooratSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPayItem
        fields = 'id', 'hazine_made_137', 'kosoorat_insurance', 'sayer_moafiat', 'manategh_tejari_moafiat', \
                 'ejtenab_maliat_mozaaf', 'naghdi_gheye_naghdi_tax',
