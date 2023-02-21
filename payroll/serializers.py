from payroll.models import Workshop, WorkshopPersonnel, Personnel, PersonnelFamily, ContractRow, HRLetter, Contract, \
    LeaveOrAbsence, Mission, ListOfPay, ListOfPayItem, WorkshopTaxRow, WorkshopTax, Loan, OptionalDeduction, LoanItem, \
    Adjustment, WorkTitle
from rest_framework import serializers


class WorkTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTitle
        fields = 'id', 'code', 'name'


class WorkShopSerializer(serializers.ModelSerializer):
    no_edit = serializers.BooleanField(source='have_list', read_only=True)
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
        fields = 'id', 'base_pay_type', 'ezafe_kari_pay_type', 'tatil_kari_pay_type', 'kasre_kar_pay_type', \
                 'shab_kari_pay_type', 'aele_mandi_pay_type', 'nobat_kari_sob_asr_pay_type', 'mission_pay_type', \
                 'nobat_kari_sob_shab_pay_type', 'nobat_kari_asr_shab_pay_type', 'nobat_kari_sob_asr_shab_pay_type', \
                 'sanavat_type', 'ezafe_kari_nerkh', 'tatil_kari_nerkh', 'kasre_kar_nerkh', 'shab_kari_nerkh', \
                 'aele_mandi_nerkh', 'nobat_kari_sob_asr_nerkh', 'nobat_kari_sob_shab_nerkh', \
                 'nobat_kari_asr_shab_nerkh', 'nobat_kari_sob_asr_shab_nerkh', 'mission_pay_nerkh', \
                 'worker_insurance_nerkh', 'employee_insurance_nerkh', 'made_86', 'hade_aksar_mashmool_bime', \
                 'moafial_maliat_haghe_bime_sahme_bime_shavande', 'unemployed_insurance_nerkh', 'is_verified', \
                 'illness_absence_in_real_work'


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
    get_child_number = serializers.IntegerField(source='child_number', read_only=True)

    class Meta:
        model = Personnel
        fields = '__all__'


class WorkshopPersonnelSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='personnel.full_name', read_only=True)
    personnel_last_name = serializers.CharField(source='personnel.last_name', read_only=True)
    personnel_identity_code = serializers.CharField(source='personnel.national_code', read_only=True)
    personnel_father = serializers.CharField(source='personnel.father_name', read_only=True)
    workshop_name = serializers.CharField(source='workshop.workshop_title', read_only=True)
    job_location_status_display = serializers.CharField(source='get_job_location_status_display', read_only=True)
    marital_display = serializers.CharField(source='personnel.get_marital_status_display', read_only=True)
    gender_display = serializers.CharField(source='personnel.get_gender_display', read_only=True)
    mobile_number = serializers.CharField(source='personnel.mobile_number_1', read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    contract_type_display = serializers.CharField(source='get_contract_type_display', read_only=True)
    get_current_insurance = serializers.CharField(source='current_insurance', read_only=True)
    get_insurance_history_total = serializers.CharField(source='insurance_history_total', read_only=True)
    employee_status_display = serializers.CharField(source='get_employee_status_display', read_only=True)
    job_group_display = serializers.CharField(source='get_job_group_display', read_only=True)
    total_insurance_month = serializers.DecimalField(source='insurance_history_total', read_only=True, max_digits=24,
                                                     decimal_places=2)
    current_insurance_month = serializers.DecimalField(source='current_insurance', read_only=True, max_digits=24,
                                                       decimal_places=2)
    quit_job = serializers.BooleanField(source='quit_job_date', read_only=True)
    insurance_history_show = serializers.IntegerField(source='quit_job_date', read_only=True)
    personnel_gender = serializers.CharField(source='personnel.gender', read_only=True)
    personnel_marital = serializers.CharField(source='personnel.marital_status', read_only=True)
    personnel_insurance = serializers.BooleanField(source='personnel.insurance', read_only=True)
    personnel_insurance_code = serializers.CharField(source='personnel.insurance_code', read_only=True)
    personnel_nationality = serializers.IntegerField(source='personnel.nationality', read_only=True)
    title_name = serializers.CharField(source='title.name', read_only=True)
    title_code = serializers.CharField(source='title.code', read_only=True)
    unverifiable = serializers.BooleanField(source='un_verifiable', read_only=True)

    class Meta:
        model = WorkshopPersonnel
        fields = '__all__'


class ContractRowSerializer(serializers.ModelSerializer):
    workshop_name = serializers.CharField(source='workshop.workshop_title', read_only=True)
    name = serializers.CharField(source='title', read_only=True)
    have_ads = serializers.BooleanField(source='have_adjustment', read_only=True)
    round_initial_amount = serializers.CharField(source='round_amount_with_comma', read_only=True)
    round_amount = serializers.CharField(source='round_now_amount_with_comma', read_only=True)
    get_status_display = serializers.CharField(source='status_display', read_only=True)
    get_verify_display = serializers.CharField(source='verify_display', read_only=True)
    get_now_date = serializers.DateField(source='now_date', read_only=True)
    get_now_amount = serializers.IntegerField(source='now_amount', read_only=True)

    class Meta:
        model = ContractRow
        fields = '__all__'


class AdjustmentSerializer(serializers.ModelSerializer):
    contract_row_display = serializers.CharField(source='contract_row.title', read_only=True)
    status_dis = serializers.CharField(source='status_display', read_only=True)

    class Meta:
        model = Adjustment
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
    workshop_id = serializers.IntegerField(source='workshop_personnel.workshop.id', read_only=True)
    personnel_insurance_month = serializers.IntegerField(source='workshop_personnel.total_insurance', read_only=True)
    unverifiable = serializers.BooleanField(source='un_verifiable', read_only=True)
    insurance_editable = serializers.BooleanField(source='is_insurance_editable', read_only=True)
    tax_editable = serializers.BooleanField(source='is_tax_editable', read_only=True)
    is_quit_job_editable = serializers.BooleanField(source='quit_job_editable', read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class HRLetterSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='contract.workshop_personnel.personnel.full_name', read_only=True)
    workshop_name = serializers.CharField(source='contract.workshop_personnel.workshop.workshop_title', read_only=True)
    is_template_display = serializers.CharField(source='get_is_template_display', read_only=True)
    contract_detail = serializers.CharField(source='contract.workshop_personnel_display', read_only=True)
    contract_code = serializers.CharField(source='contract.code', read_only=True)
    get_aele_mandi_sum = serializers.CharField(source='aele_mandi_sum', read_only=True)
    in_calculate = serializers.CharField(source='calculated', read_only=True)
    father_name = serializers.CharField(source='contract.workshop_personnel.personnel.father_name', read_only=True)
    workshop_id = serializers.IntegerField(source='contract.workshop_personnel.workshop.id', read_only=True)
    personnel_id = serializers.IntegerField(source='contract.workshop_personnel.id', read_only=True)
    personnel_father = serializers.CharField(source='contract.workshop_personnel.personnel.father_name', read_only=True)
    personnel_identity = serializers.CharField(source='contract.workshop_personnel.personnel.national_code',
                                               read_only=True)
    personnel_insurance_month = serializers.IntegerField(source='contract.workshop_personnel.total_insurance',
                                                         read_only=True)
    personnel_nationality = serializers.IntegerField(source='contract.workshop_personnel.personnel.nationality',
                                                     read_only=True)
    get_day_hourly_pay_base = serializers.IntegerField(source='day_hourly_pay_base', read_only=True)
    get_daily_pay_base = serializers.IntegerField(source='daily_pay_base', read_only=True)
    get_monthly_pay_base = serializers.IntegerField(source='monthly_pay_base', read_only=True)
    get_insurance_pay_day = serializers.IntegerField(source='insurance_pay_day', read_only=True)

    class Meta:
        model = HRLetter
        fields = '__all__'


class LeaveOrAbsenceSerializer(serializers.ModelSerializer):
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)
    person_name = serializers.CharField(source='personnel_name', read_only=True)
    by_hour = serializers.CharField(source='hour', read_only=True)
    workshop = serializers.CharField(source='workshop_personnel.workshop.workshop_title', read_only=True)
    workshop_id = serializers.IntegerField(source='workshop_personnel.workshop.id', read_only=True)

    class Meta:
        model = LeaveOrAbsence
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    loan_type_display = serializers.CharField(source='get_loan_type_display', read_only=True)
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)
    last_dept_date = serializers.CharField(source='end_date', read_only=True)
    monthly_pay = serializers.DecimalField(source='get_pay_episode', read_only=True, max_digits=24, decimal_places=6)
    months_of_pay = serializers.ListField(source='get_pay_month', read_only=True)
    workshop = serializers.CharField(source='workshop_personnel.workshop.name', read_only=True)
    workshop_id = serializers.IntegerField(source='workshop_personnel.workshop.id', read_only=True)
    editable = serializers.BooleanField(source='is_editable', read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'


class DeductionSerializer(serializers.ModelSerializer):
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)
    last_dept_date = serializers.CharField(source='end_date', read_only=True)
    monthly_pay = serializers.DecimalField(source='get_pay_episode', read_only=True, max_digits=24, decimal_places=6)
    months_of_pay = serializers.ListField(source='get_pay_month', read_only=True)
    workshop = serializers.CharField(source='workshop_personnel.workshop.name', read_only=True)
    workshop_id = serializers.IntegerField(source='workshop_personnel.workshop.id', read_only=True)
    editable = serializers.BooleanField(source='is_editable', read_only=True)

    class Meta:
        model = OptionalDeduction
        fields = '__all__'


class MissionSerializer(serializers.ModelSerializer):
    mission_type_display = serializers.CharField(source='get_mission_type_display', read_only=True)
    workshop_personnel_display = serializers.CharField(source='workshop_personnel.my_title', read_only=True)
    by_hour = serializers.CharField(source='hour', read_only=True)
    workshop = serializers.CharField(source='workshop_personnel.workshop.workshop_title', read_only=True)
    workshop_id = serializers.IntegerField(source='workshop_personnel.workshop.id', read_only=True)

    class Meta:
        model = Mission
        fields = '__all__'


class ListOfPayItemSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)
    personnel_national_code = serializers.CharField(source='workshop_personnel.personnel.national_code', read_only=True)
    hr_name = serializers.CharField(source='get_hr_letter.name', read_only=True)
    year = serializers.CharField(source='list_of_pay.year', read_only=True)
    month = serializers.CharField(source='list_of_pay.month', read_only=True)
    month_display = serializers.CharField(source='list_of_pay.month_display', read_only=True)
    workshop_display = serializers.CharField(source='workshop_personnel.workshop.workshop_title', read_only=True)
    insurance_display = serializers.CharField(source='is_insurance_display', read_only=True)
    insurance_date = serializers.DateField(source='contract.insurance_add_date', read_only=True)
    tax_date = serializers.CharField(source='contract.tax_add_date', read_only=True)
    insurance_workshop = serializers.CharField(source='workshop_personnel.current_insurance_history_in_workshop',
                                               read_only=True)
    total_mission = serializers.IntegerField(source='mission_total', read_only=True)
    hr = serializers.IntegerField(source='get_hr_letter.id', read_only=True)
    montly_pay = serializers.IntegerField(source='hoghoogh_mahane', read_only=True)
    sanavat_montly_pay = serializers.IntegerField(source='sanavat_mahane', read_only=True)
    contract_row_title = serializers.IntegerField(source='contract_row.contract_row', read_only=True)
    haghe_bime = serializers.IntegerField(source='haghe_bime_bime_shavande', read_only=True)
    start_date = serializers.CharField(source='contract.contract_from_date.__str__', read_only=True)
    work_start_date = serializers.CharField(source='contract.contract_from_date', read_only=True)
    work_title = serializers.CharField(source='workshop_personnel.title.name', read_only=True)
    get_insurance_in_workshop = serializers.CharField(source='workshop_personnel.get_insurance_in_workshop',
                                                      read_only=True)
    sanavat_mahane_real_work = serializers.CharField(source='sanavat_mahane', read_only=True)
    hoghoogh_mahane_real_work = serializers.CharField(source='hoghoogh_mahane', read_only=True)
    get_mission_total = serializers.CharField(source='mission_total', read_only=True)
    get_loan = serializers.IntegerField(source='loan_amount', read_only=True)
    get_deduction = serializers.IntegerField(source='check_and_get_optional_deduction_episode', read_only=True)
    get_dept = serializers.IntegerField(source='dept_amount', read_only=True)
    insurance_total_payment = serializers.IntegerField(source='get_insurance_total_payment', read_only=True)
    get_payable = serializers.CharField(source='payable', read_only=True)
    get_employer_tax = serializers.CharField(source='employer_insurance', read_only=True)
    get_un_employer_tax = serializers.CharField(source='un_employer_insurance', read_only=True)

    get_nobat_kari_sob_shab_total = serializers.DecimalField(source='nobat_kari_sob_shab_total',
                                                             decimal_places=2, max_digits=24, read_only=True)
    get_nobat_kari_sob_asr_total = serializers.DecimalField(source='nobat_kari_sob_asr_total',
                                                            decimal_places=2, max_digits=24, read_only=True)
    get_nobat_kari_asr_shab_total = serializers.DecimalField(source='nobat_kari_asr_shab_total',
                                                             decimal_places=2, max_digits=24, read_only=True)
    get_nobat_kari_sob_asr_shab_total = serializers.DecimalField(source='nobat_kari_sob_asr_shab_total',
                                                                 decimal_places=2, max_digits=24, read_only=True)

    get_tax_included = serializers.IntegerField(source='tax_included_payment', read_only=True)
    get_month_tax = serializers.IntegerField(source='total_tax', read_only=True)
    get_moaf_sum = serializers.IntegerField(source='moafiat_sum', read_only=True)
    get_kasre_kar_time = serializers.CharField(source='kasre_kar_time', read_only=True)
    get_ezafe_kari_time = serializers.CharField(source='ezafe_kari_time', read_only=True)
    get_tatil_kari_time = serializers.CharField(source='tatil_kari_time', read_only=True)
    get_shab_kari_time = serializers.CharField(source='shab_kari_time', read_only=True)

    get_insurance_monthly_payment = serializers.IntegerField(source='insurance_monthly_payment', read_only=True)
    get_insurance_monthly_benefit = serializers.IntegerField(source='insurance_monthly_benefit', read_only=True)
    get_insurance_total_included = serializers.IntegerField(source='insurance_total_included', read_only=True)
    get_haghe_bime_bime_shavande = serializers.IntegerField(source='haghe_bime_bime_shavande', read_only=True)

    info = serializers.JSONField(source='get_payslip', read_only=True)

    get_absence_sum = serializers.IntegerField(source='absence_sum', read_only=True)
    get_illness_sum = serializers.IntegerField(source='illness_sum', read_only=True)
    get_entitlement_sum = serializers.DecimalField(source='entitlement_sum', read_only=True, max_digits=24,
                                                   decimal_places=2)
    get_without_salary_sum = serializers.IntegerField(source='without_salary_sum', read_only=True)
    get_mission_sum = serializers.IntegerField(source='mission_sum', read_only=True)
    get_is_editable = serializers.BooleanField(source='is_editable', read_only=True)
    get_quit_job = serializers.CharField(source='quit_job', read_only=True)

    get_haghe_maskan = serializers.IntegerField(source='haghe_maskan', read_only=True)
    get_haghe_jazb = serializers.IntegerField(source='haghe_jazb', read_only=True)
    get_kharo_bar = serializers.IntegerField(source='kharo_bar', read_only=True)
    get_sayer_hr = serializers.IntegerField(source='sayer_hr', read_only=True)

    get_sanavat_notice = serializers.BooleanField(source='sanavat_notice', read_only=True)
    get_sanavat_verify = serializers.BooleanField(source='sanavat_verify', read_only=True)

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
        fields = 'paid_amount', 'personnel_name', 'id', 'unpaid_of_year', 'get_unpaid', 'payable_amout', \
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
    get_matter_47_leave_day = serializers.IntegerField(source='matter_47_leave_day', read_only=True)
    get_sanavat_notice = serializers.BooleanField(source='sanavat_notice', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = 'id', 'normal_worktime', 'real_worktime', 'personnel_name', 'mission_day', 'entitlement_leave_day', \
                 'absence_day', 'illness_leave_day', 'without_salary_leave_day', 'get_matter_47_leave_day', \
                 'get_sanavat_notice'


class ListOfPayItemLessSerializer(serializers.ModelSerializer):
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)
    is_insurance_display = serializers.CharField(source='get_is_insurance_display', read_only=True)
    title = serializers.CharField(source='workshop_personnel.title.name', read_only=True)
    get_payable = serializers.IntegerField(source='payable', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = 'total_payment', 'normal_worktime', 'real_worktime', 'personnel_name', 'is_insurance_display', 'id', \
                 'title', 'get_payable'


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
    workshop_code = serializers.CharField(source='workshop.workshop_code', read_only=True)
    month_name = serializers.CharField(source='month_display', read_only=True)
    ultimate_display = serializers.CharField(source='is_ultimate', read_only=True)
    calculate_display = serializers.CharField(source='is_use_in_calculate', read_only=True)
    get_is_editable = serializers.BooleanField(source='is_editable', read_only=True)
    contract_row = serializers.ListField(source='contract_rows', read_only=True)
    is_workshop_verified = serializers.BooleanField(source='workshop.is_verified', read_only=True)
    get_total = serializers.DictField(source='total', read_only=True)
    list_of_pay_item = ListOfPayItemSerializer(many=True)

    class Meta:
        model = ListOfPay
        fields = 'year', 'month', 'month_name', 'workshop_display', 'ultimate_display', 'workshop', 'id', 'start_date',\
                 'end_date', 'pay_done', 'calculate_display', 'name', 'ultimate', 'use_in_calculate', 'use_in_bime', \
                 'get_is_editable', 'is_workshop_verified', 'bank_pay_date', 'contract_row', 'get_total',\
                 'list_of_pay_item', 'workshop_code'


class ListOfPayItemInsuranceSerializer(serializers.ModelSerializer):
    get_data_for_insurance = serializers.JSONField(source='data_for_insurance', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = 'get_data_for_insurance'


class ListOfPayInsuranceSerializer(serializers.ModelSerializer):
    get_data_for_insurance = serializers.JSONField(source='data_for_insurance', read_only=True)
    list_of_pay_item = ListOfPayItemInsuranceSerializer()
    month_name = serializers.CharField(source='month_display', read_only=True)

    class Meta:
        model = ListOfPay
        fields = 'get_data_for_insurance', 'list_of_pay_item', 'year', 'month_name'


class WorkshopTaxRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopTaxRow
        fields = '__all__'


class LoanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanItem
        fields = '__all__'


class ListOfPayItemsAddInfoSerializer(serializers.ModelSerializer):
    get_sanavat_notice = serializers.BooleanField(source='sanavat_notice', read_only=True)
    get_kasre_kar_time = serializers.CharField(source='kasre_kar_time', read_only=True)
    personnel_name = serializers.CharField(source='workshop_personnel.personnel.full_name', read_only=True)
    get_ezafe_kari_time = serializers.CharField(source='ezafe_kari_time', read_only=True)
    get_tatil_kari_time = serializers.CharField(source='tatil_kari_time', read_only=True)
    get_shab_kari_time = serializers.CharField(source='shab_kari_time', read_only=True)
    get_absence = serializers.IntegerField(source='absence_day', read_only=True)
    get_entitlement = serializers.IntegerField(source='entitlement_leave_day', read_only=True)
    get_illness = serializers.IntegerField(source='illness_leave_day', read_only=True)
    get_with_out_salary = serializers.IntegerField(source='without_salary_leave_day', read_only=True)
    get_mission = serializers.IntegerField(source='mission_day', read_only=True)
    get_sob_asr = serializers.IntegerField(source='nobat_kari_sob_asr', read_only=True)
    get_sob_shab = serializers.IntegerField(source='nobat_kari_sob_shab', read_only=True)
    get_asr_shab = serializers.IntegerField(source='nobat_kari_asr_shab', read_only=True)
    get_sob_asr_shab = serializers.IntegerField(source='nobat_kari_sob_asr_shab', read_only=True)
    get_matter_47_leave_day = serializers.IntegerField(source='matter_47_leave_day', read_only=True)

    class Meta:
        model = ListOfPayItem
        fields = 'id', 'personnel_name', 'ezafe_kari', 'tatil_kari', 'kasre_kar', 'shab_kari', 'nobat_kari_sob_asr', \
                 'nobat_kari_sob_shab', 'nobat_kari_asr_shab', 'nobat_kari_sob_asr_shab', 'sayer_ezafat', \
                 'list_of_pay', 'calculate_payment', 'contract_row', 'mazaya_gheyr_mostamar', \
                 'hazine_made_137', 'kosoorat_insurance', 'sayer_moafiat', 'manategh_tejari_moafiat', \
                 'ejtenab_maliat_mozaaf', 'naghdi_gheye_naghdi_tax', 'cumulative_illness', 'cumulative_without_salary', \
                 'get_ezafe_kari_time', 'get_tatil_kari_time', 'get_shab_kari_time', 'get_absence', 'get_entitlement', \
                 'get_with_out_salary', 'get_illness', 'get_mission', 'get_kasre_kar_time', 'cumulative_absence', \
                 'cumulative_mission', 'cumulative_entitlement', 'get_sob_asr', 'get_sob_shab', 'get_asr_shab', \
                 'get_sob_asr_shab', 'sayer_kosoorat', 'get_matter_47_leave_day', 'get_sanavat_notice'


class ListOfPayItemsAddSayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPayItem
        fields = 'id', 'sayer_kosoorat', 'cumulative_absence ', \
                 'cumulative_mission ', 'cumulative_entitlement ', \
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
    get_is_editable = serializers.BooleanField(source='is_pay_editable', read_only=True)
    get_not_done_pay = serializers.BooleanField(source='not_done_pay', read_only=True)
    is_pay_verify = serializers.BooleanField(source='pay_verify', read_only=True)
    get_total_paid = serializers.IntegerField(source='total_paid', read_only=True)
    get_total_payable = serializers.IntegerField(source='total_payable', read_only=True)
    get_total_un_paid_of_year = serializers.IntegerField(source='total_un_paid_of_year', read_only=True)
    get_total_un_paid = serializers.IntegerField(source='total_un_paid', read_only=True)
    get_un_paid = serializers.IntegerField(source='un_paid', read_only=True)



    class Meta:
        model = ListOfPay
        fields = 'pay_done', 'id', 'bank_pay_date', 'pay_form_create_date', 'list_of_pay_item', 'workshop_name', \
                 'month_name', 'year', 'bank_pay_explanation', 'bank_pay_code', 'bank_pay_name', 'get_is_editable',\
                 'get_not_done_pay', 'name', 'year', 'is_pay_verify', 'get_total_paid', 'get_total_payable',\
                 'get_total_un_paid_of_year', 'get_total_un_paid', 'get_un_paid'


class ListOfPayItemAddPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPayItem
        fields = 'id', 'paid_amount'


class ListOfPayCopyPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPay
        fields = 'name', 'id'


class ListOfPayEditSerializer(serializers.ModelSerializer):
    get_month_display = serializers.CharField(source='month_display', read_only=True)
    get_year = serializers.CharField(source='year', read_only=True)
    workshop_name = serializers.CharField(source='workshop.workshop_title', read_only=True)

    class Meta:
        model = ListOfPay
        fields = 'id', 'name', 'use_in_calculate', 'get_month_display', 'get_year', 'workshop_name', 'workshop'


class ContractEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = 'id', 'quit_job_date', 'insurance', 'insurance_add_date', 'insurance_number', 'tax', 'tax_add_date'


class ContractEditInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = 'id', 'insurance', 'insurance_add_date', 'insurance_number'


class ContractEditTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = 'id', 'tax', 'tax_add_date'
