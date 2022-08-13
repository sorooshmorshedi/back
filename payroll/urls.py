from django.urls import path
from django.conf.urls import url

from payroll.lists.views import WorkshopListView, ContractListView, PersonnelListView, ContractRowListView
from payroll.views import WorkshopApiView, WorkshopDetail, PersonnelApiView, PersonnelDetail, \
    PersonnelFamilyApiView, PersonnelFamilyDetail, ContractRowApiView, ContractRowDetail, \
    ContractApiView, ContractDetail, PersonnelVerifyApi

urlpatterns = [
    path('workshop/', WorkshopApiView.as_view(), name='workshopApi'),
    path('workshop/<int:pk>/', WorkshopDetail.as_view(), name='workshopDetail'),

    path('personnel', PersonnelApiView.as_view(), name='personnelApi'),
    path('personnel/<int:pk>/', PersonnelDetail.as_view(), name='personnelDetail'),
    path('personnel/verify/<int:pk>/', PersonnelVerifyApi.as_view(), name='personnelVerifyApi'),

    path('personnel/family', PersonnelFamilyApiView.as_view(), name='personnelFamilyApi'),
    path('personnel/family/<int:pk>/', PersonnelFamilyDetail.as_view(), name='personnelFamilyDetail'),

    path('contract/', ContractApiView.as_view(), name='workshopPersonnelApi'),
    path('contract/<int:pk>/', ContractDetail.as_view(), name='workshopPersonnelDetail'),

    path('contract/row', ContractRowApiView.as_view(), name='contractRowApi'),
    path('contract/row/<int:pk>/', ContractRowDetail.as_view(), name='contractRowDetail'),
]

urlpatterns += [
    url(r'^workshop/all$', WorkshopListView.as_view(), name='workshopList'),
    url(r'^personnel/all$', PersonnelListView.as_view(), name='personnelList'),
    url(r'^workshop/personnel/all$', ContractListView.as_view(), name='workshopPersonnelList'),
    url(r'^personnel/family/all$', PersonnelListView.as_view(), name='personnelFamilyList'),
    url(r'^conractrow/all$', ContractRowListView.as_view(), name='contractRowList'),

]
