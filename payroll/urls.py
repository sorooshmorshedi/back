from django.urls import path
from django.conf.urls import url

from payroll.lists.export_views import WorkshopExportview, PersonnelExportview, WorkshopPersonnelExportView, \
    PersonnelFamilyExportview, ContractRowExportview, ContractExportView, LeaveOrAbsenceExportView
from payroll.lists.views import WorkshopListView, ContractListView, PersonnelListView, ContractRowListView, \
    PersonnelFamilyListView, WorkshopPersonnelListView, LeaveOrAbsenceListView, MissionListView, HRLetterListView, \
    TaxRowListView, TaxListView, ListOfPayListView, ListOfPayItemListView
from payroll.views import WorkshopApiView, WorkshopDetail, PersonnelApiView, PersonnelDetail, \
    PersonnelFamilyApiView, PersonnelFamilyDetail, ContractRowApiView, ContractRowDetail, \
    WorkshopPersonnelApiView, WorkshopPersonnelDetail, PersonnelVerifyApi, HRLetterApiView, HRLetterDetail, \
    ContractApiView, ContractDetail, LeaveOrAbsenceApiView, LeaveOrAbsenceDetail, SearchPersonnelByCode, PaymentList, \
    MissionApiView, MissionDetail, ListOfPayApiView, ListOfPayDetail, ListOfPayItemsCalculate, GetHRLetterTemplatesApi, \
    ListOfPayItemDetail, WorkshopContractRowsDetail, WorkshopTaxRowApiView, \
    WorkshopTaxRowDetail, WorkshopSettingDetail, WorkshopTaxApiView, WorkshopTaxDetail, WorkshopAllPersonnelDetail

urlpatterns = [
    path('workshop/', WorkshopApiView.as_view(), name='workshopApi'),
    path('workshop/<int:pk>/', WorkshopDetail.as_view(), name='workshopDetail'),
    path('workshop/worksho_personnel/<int:pk>/', WorkshopAllPersonnelDetail.as_view(), name='workshopAllPersonnelDetail'),
    path('workshop/setting/<int:pk>/', WorkshopSettingDetail.as_view(), name='workshopSettingDetail'),
    path('workshop/contract/row/<int:pk>/', WorkshopContractRowsDetail.as_view(), name='workshopContractRowsDetail'),

    path('tax/', WorkshopTaxApiView.as_view(), name='workshopTaxApiView'),
    path('tax/<int:pk>/', WorkshopTaxDetail.as_view(), name='workshopTaxDetail'),

    path('tax/row/', WorkshopTaxRowApiView.as_view(), name='workshopTaxRowApiView'),
    path('tax/row/<int:pk>/', WorkshopTaxRowDetail.as_view(), name='workshopTaxRowDetail'),

    path('personnel/', PersonnelApiView.as_view(), name='personnelApi'),
    path('personnel/<int:pk>/', PersonnelDetail.as_view(), name='personnelDetail'),
    path('personnel/verify/<int:pk>/', PersonnelVerifyApi.as_view(), name='personnelVerifyApi'),
    path('personnel/search/<int:code>/', SearchPersonnelByCode.as_view(), name='searchPersonnelByCode'),

    path('personnel/family/', PersonnelFamilyApiView.as_view(), name='personnelFamilyApi'),
    path('personnel/family/<int:pk>/', PersonnelFamilyDetail.as_view(), name='personnelFamilyDetail'),

    path('workshop/personnel/', WorkshopPersonnelApiView.as_view(), name='workshopPersonnelApi'),
    path('workshop/personnel/<int:pk>/', WorkshopPersonnelDetail.as_view(), name='workshopPersonnelDetail'),

    path('contract/row/', ContractRowApiView.as_view(), name='contractRowApi'),
    path('contract/row/<int:pk>/', ContractRowDetail.as_view(), name='contractRowDetail'),

    path('contract/', ContractApiView.as_view(), name='contractApi'),
    path('contract/<int:pk>/', ContractDetail.as_view(), name='contractDetail'),

    path('hrletter/', HRLetterApiView.as_view(), name='HRLetterApiView'),
    path('hrletter/templates/', GetHRLetterTemplatesApi.as_view(), name='getHRLetterTemplatesApi'),
    path('hrletter/<int:pk>/', HRLetterDetail.as_view(), name='HRLetterDetail'),

    path('absence/', LeaveOrAbsenceApiView.as_view(), name='leaveOrAbsenceApiView'),
    path('absence/<int:pk>/', LeaveOrAbsenceDetail.as_view(), name='leaveOrAbsenceDetail'),

    path('mission/', MissionApiView.as_view(), name='missionApiView'),
    path('mission/<int:pk>/', MissionDetail.as_view(), name='missionDetail'),

    path('paylist/', ListOfPayApiView.as_view(), name='listOfPayApiView'),
    path('paylist/<int:pk>/', ListOfPayDetail.as_view(), name='listOfPayDetail'),

    path('paylist/item/<int:pk>/', ListOfPayItemsCalculate.as_view(), name='listOfPayItemsCalculate'),
    path('paylist/items/<int:pk>/', ListOfPayItemDetail.as_view(), name='listOfPayItemDetail'),

    path('payment/<int:year>/<str:month>/<int:pk>/', PaymentList.as_view(), name='paymentList'),
]

urlpatterns += [
    url(r'^workshop/all$', WorkshopListView.as_view(), name='workshopList'),
    url(r'^tax/row/all$', TaxRowListView.as_view(), name='taxRowListView'),
    url(r'^tax/all$', TaxListView.as_view(), name='taxListView'),
    url(r'^personnel/all$', PersonnelListView.as_view(), name='personnelList'),
    url(r'^workshop/personnel/all$', WorkshopPersonnelListView.as_view(), name='workshopPersonnelList'),
    url(r'^personnel/family/all$', PersonnelFamilyListView.as_view(), name='personnelFamilyList'),
    url(r'^conractrow/all$', ContractRowListView.as_view(), name='contractRowList'),
    url(r'^contract/all$', ContractListView.as_view(), name='contractRowList'),
    url(r'^absence/all$', LeaveOrAbsenceListView.as_view(), name='leaveOrAbsenceList'),
    url(r'^mission/all$', MissionListView.as_view(), name='missionListView'),
    url(r'^hrletter/all$', HRLetterListView.as_view(), name='hrLetterListView'),
    url(r'^listOfPay/all$', ListOfPayListView.as_view(), name='listOfPayListView'),
    url(r'^listOfPayItem/all$', ListOfPayItemListView.as_view(), name='listOfPayItemListView'),

    url(r'^workshop/all/(?P<export_type>\S+)', WorkshopExportview.as_view(), name=''),
    url(r'^personnel/all/(?P<export_type>\S+)', PersonnelExportview.as_view(), name=''),
    url(r'^workshop/personnel/all/(?P<export_type>\S+)', WorkshopPersonnelExportView.as_view(), name=''),
    url(r'^personnel/family/all/(?P<export_type>\S+)', PersonnelFamilyExportview.as_view(), name=''),
    url(r'^contractrow/all/(?P<export_type>\S+)', ContractRowExportview.as_view(), name=''),
    url(r'^contract/all/(?P<export_type>\S+)', ContractExportView.as_view(), name=''),
    url(r'^absence/all/(?P<export_type>\S+)', LeaveOrAbsenceExportView.as_view(), name=''),

]
