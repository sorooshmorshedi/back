from django.urls import path
from django.conf.urls import url

from payroll.lists.export_views import WorkshopExportview, PersonnelExportview, WorkshopPersonnelExportView, \
    PersonnelFamilyExportview, ContractRowExportview, ContractExportView, LeaveOrAbsenceExportView
from payroll.lists.views import WorkshopListView, ContractListView, PersonnelListView, ContractRowListView
from payroll.views import WorkshopApiView, WorkshopDetail, PersonnelApiView, PersonnelDetail, \
    PersonnelFamilyApiView, PersonnelFamilyDetail, ContractRowApiView, ContractRowDetail, \
    WorkshopPersonnelApiView, WorkshopPersonnelDetail, PersonnelVerifyApi, HRLetterApiView, HRLetterDetail, \
    ContractApiView, ContractDetail, LeaveOrAbsenceApiView, LeaveOrAbsenceDetail, SearchPersonnelByCode

urlpatterns = [
    path('workshop/', WorkshopApiView.as_view(), name='workshopApi'),
    path('workshop/<int:pk>/', WorkshopDetail.as_view(), name='workshopDetail'),

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
    path('hrletter/<int:pk>/', HRLetterDetail.as_view(), name='HRLetterDetail'),

    path('absence/', LeaveOrAbsenceApiView.as_view(), name='leaveOrAbsenceApiView'),
    path('absence/<int:pk>/', LeaveOrAbsenceDetail.as_view(), name='leaveOrAbsenceDetail'),
]

urlpatterns += [
    url(r'^workshop/all$', WorkshopListView.as_view(), name='workshopList'),
    url(r'^personnel/all$', PersonnelListView.as_view(), name='personnelList'),
    url(r'^workshop/personnel/all$', WorkshopListView.as_view(), name='workshopPersonnelList'),
    url(r'^personnel/family/all$', PersonnelListView.as_view(), name='personnelFamilyList'),
    url(r'^conractrow/all$', ContractRowListView.as_view(), name='contractRowList'),
    url(r'^contract/all$', ContractListView.as_view(), name='contractRowList'),
    url(r'^workshop/all/(?P<export_type>\S+)', WorkshopExportview.as_view(), name=''),
    url(r'^personnel/all/(?P<export_type>\S+)', PersonnelExportview.as_view(), name=''),
    url(r'^workshop/personnel/all/(?P<export_type>\S+)', WorkshopPersonnelExportView.as_view(), name=''),
    url(r'^personnel/family/all/(?P<export_type>\S+)', PersonnelFamilyExportview.as_view(), name=''),
    url(r'^contractrow/all/(?P<export_type>\S+)', ContractRowExportview.as_view(), name=''),
    url(r'^contract/all/(?P<export_type>\S+)', ContractExportView.as_view(), name=''),
    url(r'^absence/all/(?P<export_type>\S+)', LeaveOrAbsenceExportView.as_view(), name=''),

]
