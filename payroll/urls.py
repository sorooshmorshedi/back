from django.urls import path
from django.conf.urls import url

from payroll.lists.views import WorkshopListView, WorkshopPersonnelListView, PersonnelListView, ContractRowListView, \
    ContractTimeListView
from payroll.views import WorkshopApiView, WorkshopDetail, PersonnelApiView, PersonnelDetail, \
    PersonnelFamilyApiView, PersonnelFamilyDetail, ContractRowApiView, ContractRowDetail, \
    WorkshopPersonnelApiView, WorkshopPersonnelDetail, ContractTimeApiView, ContractTimeDetail

urlpatterns = [
    path('workshop/', WorkshopApiView.as_view(), name='workshopApi'),
    path('workshop/<int:pk>/', WorkshopDetail.as_view(), name='workshopDetail'),

    path('personnel', PersonnelApiView.as_view(), name='personnelApi'),
    path('personnel/<int:pk>/', PersonnelDetail.as_view(), name='personnelDetail'),

    path('personnel/family', PersonnelFamilyApiView.as_view(), name='personnelFamilyApi'),
    path('personnel/family/<int:pk>/', PersonnelFamilyDetail.as_view(), name='personnelFamilyDetail'),

    path('workshop/personnel/', WorkshopPersonnelApiView.as_view(), name='workshopPersonnelApi'),
    path('workshop/personnel/<int:pk>/', WorkshopPersonnelDetail.as_view(), name='workshopPersonnelDetail'),

    path('contract/row', ContractRowApiView.as_view(), name='contractRowApi'),
    path('contract/row/<int:pk>/', ContractRowDetail.as_view(), name='contractRowDetail'),

    path('contract/time', ContractTimeApiView.as_view(), name='contractTimeApi'),
    path('contract/time/<int:pk>/', ContractTimeDetail.as_view(), name='contractTimeDetail')
]

urlpatterns += [
    url(r'^workshop/all$', WorkshopListView.as_view(), name='workshopList'),
    url(r'^personnel/all$', PersonnelListView.as_view(), name='personnelList'),
    url(r'^workshop/personnel/all$', WorkshopPersonnelListView.as_view(), name='workshopPersonnelList'),
    url(r'^personnel/family/all$', PersonnelListView.as_view(), name='personnelFamilyList'),
    url(r'^conractrow/all$', ContractRowListView.as_view(), name='contractRowList'),
    url(r'^conract/time/all$', ContractTimeListView.as_view(), name='contractTimeList'),

]
