
from payroll.models import Workshop, WorkshopPersonnel, Personnel, PersonnelFamily, ContractRow, HRLetter, Contract, \
    LeaveOrAbsence, Mission, ListOfPay, ListOfPayItem, WorkshopTaxRow, WorkshopTax, Loan, OptionalDeduction, LoanItem
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
    verified = serializers.BooleanField(source='is_personnel_verified', read_only=True)
    bank_name = serializers.CharField(source='get_account_bank_name_display', read_only=True)
    is_insurance = serializers.CharField(source='insurance_display', read_only=True)
    is_verify = serializers.CharField(source='verify_display', read_only=True)
    is_active = serializers.CharField(source='active_display', read_only=True)
    birth_city = serializers.CharField(source='location_of_birth', read_only=True)
    exportation_city = serializers.CharField(source='location_of_exportation', read_only=True)
    exportation_sector = serializers.CharField(source='sector_of_exportation', read_only=True)

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
    total_insurance_month = serializers.IntegerField(source='insurance_history_total', read_only=True)
    current_insurance_month = serializers.IntegerField(source='current_insurance', read_only=True)
    quit_job = serializers.BooleanField(source='quit_job_date', read_only=True)
    insurance_history_show = serializers.IntegerField(source='quit_job_date', read_only=True)

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
    insurance_display = serializers.CharField(source='is_insurance_display', read_only=True)

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
    person_name = serializers.CharField(source='personnel_name', read_only=True)

    class Meta:
        model = LeaveOrAbsence
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    loan_type_display = serializers.CharField(source='get_loan_type_display', read_only=True)
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)
    last_dept_date = serializers.CharField(source='end_date', read_only=True)
    monthly_pay = serializers.DecimalField(source='get_pay_episode', read_only=True, max_digits=24, decimal_places=6)
    months_of_pay = serializers.ListField(source='get_pay_month', read_only=True)


    class Meta:
        model = Loan
        fields = '__all__'


class DeductionSerializer(serializers.ModelSerializer):
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)
    last_dept_date = serializers.CharField(source='end_date', read_only=True)
    monthly_pay = serializers.DecimalField(source='get_pay_episode', read_only=True, max_digits=24, decimal_places=6)
    months_of_pay = serializers.ListField(source='get_pay_month', read_only=True)

    class Meta:
        model = OptionalDeduction
        fields = '__all__'


class MissionSerializer(serializers.ModelSerializer):
    mission_type_display = serializers.CharField(source='get_mission_type_display', read_only=True)
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)

    class Meta:
        model = Mission
        fields = '__all__'


class ListOfPayItemSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)
    year = serializers.CharField(source='list_of_pay.year', read_only=True)
    month = serializers.CharField(source='list_of_pay.month', read_only=True)
    month_display = serializers.CharField(source='list_of_pay.month_display', read_only=True)
    workshop_display = serializers.CharField(source='workshop_personnel.workshop.workshop_title', read_only=True)
    is_insurance_display = serializers.CharField(source='get_is_insurance_display', read_only=True)
    insurance_workshop = serializers.CharField(source='workshop_personnel.current_insurance_history_in_workshop',
                                               read_only=True)
    total_mission = serializers.IntegerField(source='mission_total', read_only=True)
    montly_pay = serializers.IntegerField(source='hoghoogh_mahane', read_only=True)
    sanavat_montly_pay = serializers.IntegerField(source='sanavat_mahane', read_only=True)
    contract_row_title = serializers.IntegerField(source='contract_row.contract_row', read_only=True)
    haghe_bime = serializers.IntegerField(source='haghe_bime_bime_shavande', read_only=True)
    start_date = serializers.CharField(source='contract.contract_from_date.__str__', read_only=True)
    work_title = serializers.CharField(source='workshop_personnel.work_title', read_only=True)
    get_insurance_in_workshop = serializers.CharField(source='workshop_personnel.get_insurance_in_workshop', read_only=True)
    sanavat_mahane_real_work = serializers.CharField(source='sanavat_mahane', read_only=True)
    hoghoogh_mahane_real_work = serializers.CharField(source='hoghoogh_mahane', read_only=True)
    get_mission_total = serializers.CharField(source='mission_total', read_only=True)
    get_loan = serializers.CharField(source='check_and_get_loan_episode', read_only=True)
    get_deduction = serializers.CharField(source='check_and_get_optional_deduction_episode', read_only=True)
    get_dept = serializers.CharField(source='check_and_get_dept_episode', read_only=True)
    get_payable = serializers.CharField(source='payable', read_only=True)
    get_employer_tax = serializers.CharField(source='employer_insurance', read_only=True)
    get_un_employer_tax = serializers.CharField(source='un_employer_insurance', read_only=True)

    get_tax_included = serializers.CharField(source='tax_included_payment', read_only=True)
    get_month_tax = serializers.CharField(source='calculate_month_tax', read_only=True)
    get_moaf_sum = serializers.CharField(source='moaf_sum', read_only=True)

    get_insurance_monthly_payment = serializers.CharField(source='insurance_monthly_payment', read_only=True)
    get_insurance_monthly_benefit = serializers.CharField(source='insurance_monthly_benefit', read_only=True)
    get_insurance_total_included = serializers.CharField(source='insurance_total_included', read_only=True)
    get_haghe_bime_bime_shavande = serializers.CharField(source='haghe_bime_bime_shavande', read_only=True)

    info = serializers.JSONField(source='get_payslip', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = '__all__'

class ListOfPayItemBankSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)
    get_unpaid = serializers.IntegerField(source='unpaid', read_only=True)
    unpaid_of_year = serializers.IntegerField(source='get_unpaid_of_year', read_only=True)
    payable_amout = serializers.IntegerField(source='payable', read_only=True)
    loan_amount = serializers.IntegerField(source='check_and_get_loan_episode', read_only=True)
    dept_amount = serializers.IntegerField(source='check_and_get_dept_episode', read_only=True)
    get_total_unpaid = serializers.IntegerField(source='total_unpaid', read_only=True)
    class Meta:
        model = ListOfPayItem
        fields = 'paid_amount', 'personnel_name', 'id', 'unpaid_of_year', 'get_unpaid', 'payable_amout',\
                 'loan_amount', 'dept_amount', 'get_total_unpaid'

class ListOfPayItemPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPayItem
        fields = 'id', 'paid_amount'

class ListOfPayBankSerializer(serializers.ModelSerializer):
    list_of_pay_item = ListOfPayItemBankSerializer(many=True)
    workshop_display = serializers.CharField(source='workshop.workshop_title', read_only=True)
    month_name = serializers.CharField(source='month_display', read_only=True)
    ultimate_display = serializers.CharField(source='is_ultimate', read_only=True)
    class Meta:
        model = ListOfPay
        fields = '__all__'

class ListOfPayItemNormalSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = 'id', 'normal_worktime', 'real_worktime', 'personnel_name'


class ListOfPayItemLessSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)
    is_insurance_display = serializers.CharField(source='get_is_insurance_display', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = 'total_payment', 'normal_worktime', 'real_worktime', 'personnel_name', 'is_insurance_display', 'id'

class ListOfPaySerializer(serializers.ModelSerializer):
    list_of_pay_item = ListOfPayItemNormalSerializer(many=True)
    workshop_display = serializers.CharField(source='workshop.workshop_title', read_only=True)
    month_name = serializers.CharField(source='month_display', read_only=True)
    ultimate_display = serializers.CharField(source='is_ultimate', read_only=True)

    class Meta:
        model = ListOfPay
        fields = '__all__'

class ListOfPayLessSerializer(serializers.ModelSerializer):
    workshop_display = serializers.CharField(source='workshop.workshop_title', read_only=True)
    month_name = serializers.CharField(source='month_display', read_only=True)
    ultimate_display = serializers.CharField(source='is_ultimate', read_only=True)
    calculate_display = serializers.CharField(source='is_use_in_calculate', read_only=True)

    class Meta:
        model = ListOfPay
        fields = 'year', 'month', 'month_name', 'workshop_display', 'ultimate_display', 'workshop', 'id', 'start_date',\
                 'end_date', 'pay_done', 'calculate_display', 'ultimate_display', 'name'


class ListOfPayInsuranceSerializer(serializers.ModelSerializer):
    get_data_for_insurance = serializers.JSONField(source='data_for_insurance', read_only=True)

    class Meta:
        model = ListOfPay
        fields = 'get_data_for_insurance'

class ListOfPayItemInsuranceSerializer(serializers.ModelSerializer):
    get_data_for_insurance = serializers.JSONField(source='data_for_insurance', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = 'get_data_for_insurance'



class WorkshopTaxRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopTaxRow
        fields = '__all__'

class LoanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanItem
        fields = '__all__'


class ListOfPayItemsAddInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPayItem
        fields = 'id', 'ezafe_kari', 'tatil_kari', 'kasre_kar', 'shab_kari', 'nobat_kari_sob_asr', \
                 'nobat_kari_sob_shab', 'nobat_kari_asr_shab', 'nobat_kari_sob_asr_shab', 'sayer_ezafat', \
                 'list_of_pay', 'calculate_payment', 'contract_row', 'mazaya_gheyr_mostamar',\
                 'hazine_made_137', 'kosoorat_insurance', 'sayer_moafiat', 'manategh_tejari_moafiat', \
                 'ejtenab_maliat_mozaaf', 'naghdi_gheye_naghdi_tax', 'cumulative_illness', 'cumulative_without_salary',\
                 'cumulative_entitlement', 'cumulative_mission', 'cumulative_absence', 'sayer_kosoorat'

class ListOfPayItemsAddSayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPayItem
        fields = 'id' , 'sayer_kosoorat', 'cumulative_absence ', \
                        'cumulative_mission ', 'cumulative_entitlement ',\
                        'cumulative_illness ', 'cumulative_without_salary '


class PersonTaxSerializer(serializers.ModelSerializer):
    get_data_for_tax = serializers.JSONField(source='data_for_tax', read_only=True)
    class Meta:
        model = ListOfPayItem
        fields = 'get_data_for_tax', 'id', 'data_for_tax'

class TaxSerializer(serializers.ModelSerializer):
    get_data_for_tax = serializers.JSONField(source='data_for_tax', read_only=True)
    class Meta:
        model = ListOfPay
        fields = 'id', 'data_for_tax', 'get_data_for_tax'



class ListOfPayPaySerializer(serializers.ModelSerializer):
    list_of_pay_item = ListOfPayItemBankSerializer(many=True, read_only=True)
    workshop_name = serializers.CharField(source='workshop.workshop_title', read_only=True)
    month_name = serializers.CharField(source='month_display', read_only=True)
    class Meta:
        model = ListOfPay
        fields = 'pay_done', 'id', 'bank_pay_date', 'pay_form_create_date', 'list_of_pay_item', 'workshop_name',\
                 'month_name', 'year'


class ListOfPayItemAddPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPayItem
        fields = 'id', 'paid_amount'


class ListOfPayCopyPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPay
        fields = 'name', 'id'


