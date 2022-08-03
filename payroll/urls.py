from django.urls import path

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
