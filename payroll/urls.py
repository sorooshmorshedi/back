from django.urls import path
from django.conf.urls import url

from payroll.lists.export_views import WorkshopExportview, PersonnelExportview, WorkshopPersonnelExportView, \
    PersonnelFamilyExportview, ContractRowExportview, ContractExportView, LeaveOrAbsenceExportView, \
    AbsenceRequestExportView, MissionExportView, MissionRequestExportView, ContractFormExportView, HRLetterExportView, \
    LoanExportView, DeductionExportView, LoanRequestExportView, PayslipExportView, BankReportExportView, \
    PayrollExportView, LoanItemExportView, PersonInsuranceReportExportView, WorkshopInsuranceReportExportView, \
    PersonTaxReportExportView, TaxReportExportView, MonthTaxReportExportView, AbsenceReportExportView, \
    NewPersonTaxReportExportView, SaveLeaveReportExportView, PayFormExportView, SettlementExportView, \
    AccountBalanceReportExportView, EydiReportExportView, SanavatReportExportView, AdjustmentExportView
from payroll.lists.views import WorkshopListView, ContractListView, PersonnelListView, ContractRowListView, \
    PersonnelFamilyListView, WorkshopPersonnelListView, LeaveOrAbsenceListView, MissionListView, HRLetterListView, \
    TaxRowListView, TaxListView, ListOfPayListView, ListOfPayItemListView, LoanListView, DeductionListView, \
    LoanItemListView, ListOfPayItemLessListView, write_tax_diskette, \
    write_person_insurance_diskette, \
    write_insurance_diskette, write_summary_tax_diskette, TaxMoafListView, write_new_person_diskette, AdjustmentListView
from payroll.views import WorkshopApiView, WorkshopDetail, PersonnelApiView, PersonnelDetail, \
    PersonnelFamilyApiView, PersonnelFamilyDetail, ContractRowApiView, ContractRowDetail, \
    WorkshopPersonnelApiView, WorkshopPersonnelDetail, PersonnelVerifyApi, HRLetterApiView, HRLetterDetail, \
    ContractApiView, ContractDetail, LeaveOrAbsenceApiView, LeaveOrAbsenceDetail, SearchPersonnelByCode, PaymentList, \
    MissionApiView, MissionDetail, ListOfPayApiView, ListOfPayDetail, ListOfPayItemsCalculate, GetHRLetterTemplatesApi, \
    ListOfPayItemDetail, WorkshopContractRowsDetail, WorkshopTaxRowApiView, \
    WorkshopTaxRowDetail, WorkshopSettingDetail, WorkshopTaxApiView, WorkshopTaxDetail, WorkshopAllPersonnelDetail, \
    LoanApiView, LoanDetail, PersonnelLoanDetail, DeductionApiView, DeductionDetail, PersonnelDeductionDetail, \
    TemplateDeductionDetail, LoanItemDetail, ListOfPayLessDetail, PayItemDetail, ListOfPayBankDetail, PayAPI, \
    ListOfPayPaymentAPI, ListOfPayItemPaymentAPI, WorkshopListOfPayApiView, ListOfPayCopy, PersonnelUnVerifyApi, \
    PersonnelFamilyVerifyApi, PersonnelFamilyUnVerifyApi, ContractRowVerifyApi, ContractRowUnVerifyApi, \
    AdjustmentApiView, AdjustmentDetail, ContractRowAdjustmentDetail, PaymentVerifyApiView, WorkshopPersonnelVerifyApi, \
    WorkshopPersonnelUnVerifyApi, ContractRowUnActiveApi, ContractRowActiveApi, WorkshopVerifyApi, WorkshopUnVerifyApi, \
    LeaveOrAbsenceVerifyApi, LeaveOrAbsenceUnVerifyApi, MissionVerifyApi, MissionUnVerifyApi, ContractVerifyApi, \
    ContractUnVerifyApi

urlpatterns = [
    path('workshop/', WorkshopApiView.as_view(), name='workshopApi'),
    path('workshop/<int:pk>/', WorkshopDetail.as_view(), name='workshopDetail'),
    path('workshop/workshop_personnel/<int:pk>/', WorkshopAllPersonnelDetail.as_view(), name='workshopAllPersonnelDetail'),
    path('workshop/setting/<int:pk>/', WorkshopSettingDetail.as_view(), name='workshopSettingDetail'),
    path('workshop/contract/row/<int:pk>/', WorkshopContractRowsDetail.as_view(), name='workshopContractRowsDetail'),
    path('workshop/verify/<int:pk>/', WorkshopVerifyApi.as_view(), name='workshopVerifyApi'),
    path('workshop/unverify/<int:pk>/', WorkshopUnVerifyApi.as_view(), name='workshopUnVerifyApi'),

    path('tax/', WorkshopTaxApiView.as_view(), name='workshopTaxApiView'),
    path('tax/<int:pk>/', WorkshopTaxDetail.as_view(), name='workshopTaxDetail'),

    path('loan/', LoanApiView.as_view(), name='loanApiView'),
    path('loan/<int:pk>/', LoanDetail.as_view(), name='loanDetail'),
    path('loan/item/<int:pk>/', LoanItemDetail.as_view(), name='loanItemDetail'),
    path('personnel/loan/<int:pk>/', PersonnelLoanDetail.as_view(), name='personnelLoanDetail'),

    path('deduction/', DeductionApiView.as_view(), name='deductionApiView'),
    path('deduction/<int:pk>/', DeductionDetail.as_view(), name='deductionDetail'),
    path('deduction/template/', TemplateDeductionDetail.as_view(), name='templateDeductionDetail'),
    path('personnel/deduction/<int:pk>/', PersonnelDeductionDetail.as_view(), name='personnelDeductionDetail'),

    path('tax/row/', WorkshopTaxRowApiView.as_view(), name='workshopTaxRowApiView'),
    path('tax/row/<int:pk>/', WorkshopTaxRowDetail.as_view(), name='workshopTaxRowDetail'),

    path('personnel/', PersonnelApiView.as_view(), name='personnelApi'),
    path('personnel/<int:pk>/', PersonnelDetail.as_view(), name='personnelDetail'),
    path('personnel/verify/<int:pk>/', PersonnelVerifyApi.as_view(), name='personnelVerifyApi'),
    path('personnel/unverify/<int:pk>/', PersonnelUnVerifyApi.as_view(), name='personnelUnVerifyApi'),
    path('personnel/search/<int:code>/', SearchPersonnelByCode.as_view(), name='searchPersonnelByCode'),

    path('personnel/family/', PersonnelFamilyApiView.as_view(), name='personnelFamilyApi'),
    path('personnel/family/<int:pk>/', PersonnelFamilyDetail.as_view(), name='personnelFamilyDetail'),
    path('personnel/family/verify/<int:pk>/', PersonnelFamilyVerifyApi.as_view(), name='personnelFamilyVerifyApi'),
    path('personnel/family/unverify/<int:pk>/', PersonnelFamilyUnVerifyApi.as_view(), name='personnelFamilyUnVerifyApi'),

    path('workshop/personnel/', WorkshopPersonnelApiView.as_view(), name='workshopPersonnelApi'),
    path('workshop/personnel/<int:pk>/', WorkshopPersonnelDetail.as_view(), name='workshopPersonnelDetail'),
    path('workshopPersonnel/verify/<int:pk>/', WorkshopPersonnelVerifyApi.as_view(),
         name='workshopPersonnelVerifyApi'),
    path('workshopPersonnel/unverify/<int:pk>/', WorkshopPersonnelUnVerifyApi.as_view(),
         name='workshopPersonnelUnVerifyApi'),

    path('contract/row/', ContractRowApiView.as_view(), name='contractRowApi'),
    path('contract/row/<int:pk>/', ContractRowDetail.as_view(), name='contractRowDetail'),
    path('contract/row/verify/<int:pk>/', ContractRowVerifyApi.as_view(), name='contractRowVerifyApi'),
    path('contract/row/unverify/<int:pk>/', ContractRowUnVerifyApi.as_view(), name='contractRowUnVerifyApi'),
    path('contract/row/active/<int:pk>/', ContractRowActiveApi.as_view(), name='contractRowActiveApi'),
    path('contract/row/unactive/<int:pk>/', ContractRowUnActiveApi.as_view(), name='contractRowUnActiveApi'),
    path('adjustment/', AdjustmentApiView.as_view(), name='adjustmentApiView'),
    path('adjustment/<int:pk>/', AdjustmentDetail.as_view(), name='adjustmentDetail'),
    path('contract_row/adjustment/<int:pk>/', ContractRowAdjustmentDetail.as_view(), name='contractRowAdjustmentDetail'),

    path('contract/', ContractApiView.as_view(), name='contractApi'),
    path('contract/<int:pk>/', ContractDetail.as_view(), name='contractDetail'),
    path('contract/verify/<int:pk>/', ContractVerifyApi.as_view(), name='contractVerifyApi'),
    path('contract/unverify/<int:pk>/', ContractUnVerifyApi.as_view(), name='contractUnVerifyApi'),

    path('hrletter/', HRLetterApiView.as_view(), name='HRLetterApiView'),
    path('hrletter/templates/', GetHRLetterTemplatesApi.as_view(), name='getHRLetterTemplatesApi'),
    path('hrletter/<int:pk>/', HRLetterDetail.as_view(), name='HRLetterDetail'),

    path('absence/', LeaveOrAbsenceApiView.as_view(), name='leaveOrAbsenceApiView'),
    path('absence/<int:pk>/', LeaveOrAbsenceDetail.as_view(), name='leaveOrAbsenceDetail'),
    path('absence/verify/<int:pk>/', LeaveOrAbsenceVerifyApi.as_view(), name='leaveOrAbsenceVerifyApi'),
    path('absence/unverify/<int:pk>/', LeaveOrAbsenceUnVerifyApi.as_view(), name='leaveOrAbsenceUnVerifyApi'),

    path('mission/', MissionApiView.as_view(), name='missionApiView'),
    path('mission/<int:pk>/', MissionDetail.as_view(), name='missionDetail'),
    path('mission/verify/<int:pk>/', MissionVerifyApi.as_view(), name='missionVerifyApi'),
    path('mission/unverify/<int:pk>/', MissionUnVerifyApi.as_view(), name='missionUnVerifyApi'),

    path('paylist/', ListOfPayApiView.as_view(), name='listOfPayApiView'),
    path('paylist/<int:pk>/', ListOfPayDetail.as_view(), name='listOfPayDetail'),
    path('paylist/less/<int:pk>/', ListOfPayLessDetail.as_view(), name='listOfPayLessDetail'),

    path('pay/<int:pk>/', PayAPI.as_view(), name='payAPI'),
    path('paylist/item/<int:pk>/', ListOfPayItemsCalculate.as_view(), name='listOfPayItemsCalculate'),
    path('paylist/bank/<int:pk>/', ListOfPayBankDetail.as_view(), name='listOfPayBankDetail'),
    path('paylist/items/<int:pk>/', ListOfPayItemDetail.as_view(), name='listOfPayItemDetail'),
    path('paylist/item/detail/<int:pk>/', PayItemDetail.as_view(), name='payItemDetail'),

    path('payment/<int:year>/<int:month>/<int:pk>/', PaymentList.as_view(), name='paymentList'),
    path('PaymentVerify/<int:year>/<int:month>/<int:pk>/', PaymentVerifyApiView.as_view(), name='paymentVerifyApiView'),

    path('diskette/tax/<int:pk>/', write_tax_diskette),
    path('diskette/tax/newPerson/<int:pk>/', write_new_person_diskette),
    path('diskette/tax/summary/<int:pk>/', write_summary_tax_diskette),

    path('diskette/insurance/<int:pk>/', write_insurance_diskette),
    path('diskette/insurance/person/<int:pk>/', write_person_insurance_diskette),

    path('absence/report/<int:year>/<str:month>/', AbsenceReportExportView.as_view()),
    path('saveLeave/report/<int:year>/<str:month>/', SaveLeaveReportExportView.as_view()),
    path('eydi/report/<int:year>/<str:month>/', EydiReportExportView.as_view()),
    path('sanavat/report/<int:year>/<str:month>/', SanavatReportExportView.as_view()),
    path('settlement/<int:personnel>/<str:export_type>', SettlementExportView.as_view()),

    path('listOfPay/pay/<int:pk>/', ListOfPayPaymentAPI.as_view(), name='listOfPayPaymentAPI'),
    path('listOfPayItem/pay/<int:pk>/', ListOfPayItemPaymentAPI.as_view(), name='listOfPayItemPaymentAPI'),

    path('listOfPay/workshop/<int:pk>/<int:month>/<str:year>/', WorkshopListOfPayApiView.as_view(),
         name='workshopListOfPayApiView'),
    path('listOfPay/copy/<int:pk>/', ListOfPayCopy.as_view(), name='listOfPayCopy'),

]

urlpatterns += [
    url(r'^workshop/all$', WorkshopListView.as_view(), name='workshopList'),
    url(r'^tax/row/all$', TaxRowListView.as_view(), name='taxRowListView'),
    url(r'^tax/all$', TaxMoafListView.as_view(), name='taxListView'),
    url(r'^personnel/all$', PersonnelListView.as_view(), name='personnelList'),
    url(r'^workshop/personnel/all$', WorkshopPersonnelListView.as_view(), name='workshopPersonnelList'),
    url(r'^personnel/family/all$', PersonnelFamilyListView.as_view(), name='personnelFamilyList'),
    url(r'^contractRows/all$', ContractRowListView.as_view(), name='contractRowList'),
    url(r'^adjustment/all$', AdjustmentListView.as_view(), name='adjustmentListView'),
    url(r'^contract/all$', ContractListView.as_view(), name='contractRowList'),
    url(r'^absence/all$', LeaveOrAbsenceListView.as_view(), name='leaveOrAbsenceList'),
    url(r'^mission/all$', MissionListView.as_view(), name='missionListView'),
    url(r'^hrletter/all$', HRLetterListView.as_view(), name='hrLetterListView'),
    url(r'^listOfPay/all$', ListOfPayListView.as_view(), name='listOfPayListView'),
    url(r'^listOfPayItem/all$', ListOfPayItemListView.as_view(), name='listOfPayItemListView'),
    url(r'^listOfPayItem/less$', ListOfPayItemLessListView.as_view(), name='listOfPayItemListView'),
    url(r'^loan/item/all$', LoanItemListView.as_view(), name='loanItemListView'),
    url(r'^loan/all$', LoanListView.as_view(), name='loanListView'),
    url(r'^deduction/all$', DeductionListView.as_view(), name='deductionListView'),

    url(r'^workshop/all/(?P<export_type>\S+)', WorkshopExportview.as_view(), name=''),
    url(r'^personnel/all/(?P<export_type>\S+)', PersonnelExportview.as_view(), name=''),
    url(r'^workshop/personnel/all/(?P<export_type>\S+)', WorkshopPersonnelExportView.as_view(), name=''),
    url(r'^personnel/family/all/(?P<export_type>\S+)', PersonnelFamilyExportview.as_view(), name=''),
    url(r'^contractRows/all/(?P<export_type>\S+)', ContractRowExportview.as_view(), name=''),
    url(r'^adjustment/all/(?P<export_type>\S+)', AdjustmentExportView.as_view(), name=''),
    url(r'^contract/all/(?P<export_type>\S+)', ContractExportView.as_view(), name=''),
    url(r'^contract/form/(?P<export_type>\S+)', ContractFormExportView.as_view(), name=''),
    url(r'^absence/all/(?P<export_type>\S+)', LeaveOrAbsenceExportView.as_view(), name=''),
    url(r'^hrletter/all/(?P<export_type>\S+)', HRLetterExportView.as_view(), name=''),
    url(r'^absence/request/(?P<export_type>\S+)', AbsenceRequestExportView.as_view(), name=''),
    url(r'^mission/all/(?P<export_type>\S+)', MissionExportView.as_view(), name=''),
    url(r'^mission/request/(?P<export_type>\S+)', MissionRequestExportView.as_view(), name=''),
    url(r'^loan/all/(?P<export_type>\S+)', LoanExportView.as_view(), name=''),
    url(r'^loan/item/(?P<export_type>\S+)', LoanItemExportView.as_view(), name=''),
    url(r'^loan/request/(?P<export_type>\S+)', LoanRequestExportView.as_view(), name=''),
    url(r'^deduction/all/(?P<export_type>\S+)', DeductionExportView.as_view(), name=''),
    url(r'^payslip/(?P<export_type>\S+)', PayslipExportView.as_view(), name=''),
    url(r'^payForm/(?P<export_type>\S+)', PayFormExportView.as_view(), name=''),
    url(r'^bankReport/(?P<export_type>\S+)', BankReportExportView.as_view(), name=''),
    url(r'^total/insurance/report/(?P<export_type>\S+)', WorkshopInsuranceReportExportView.as_view(), name=''),
    url(r'^person/insurance/report/(?P<export_type>\S+)', PersonInsuranceReportExportView.as_view(), name=''),
    url(r'^tax/report/(?P<export_type>\S+)', TaxReportExportView.as_view(), name=''),
    url(r'^personTax/report/(?P<export_type>\S+)', PersonTaxReportExportView.as_view(), name=''),
    url(r'^month/tax/(?P<export_type>\S+)', MonthTaxReportExportView.as_view(), name=''),
    url(r'^diskette/person/(?P<export_type>\S+)', NewPersonTaxReportExportView.as_view(), name=''),
    url(r'^payroll/(?P<export_type>\S+)', PayrollExportView.as_view(), name=''),
    url(r'^balance/(?P<export_type>\S+)', AccountBalanceReportExportView.as_view(), name=''),

]
