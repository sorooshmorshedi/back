from django.conf.urls import url

from wares.views import WareListCreate, WareDetail, WarehouseListCreate, \
    UnitListCreate, UnitDetail, WarehouseDetail

urlpatterns = [
    url(r'^wares$', WareListCreate.as_view(), name='Wares'),
    url(r'^wares/(?P<pk>[0-9]+)$', WareDetail.as_view(), name='WareDetail'),

    url(r'^units$', UnitListCreate.as_view(), name='units'),
    url(r'^units/(?P<pk>[0-9]+)$', UnitDetail.as_view(), name='unitDetail'),

    url(r'^warehouses$', WarehouseListCreate.as_view(), name='warehouse'),
    url(r'^warehouses/(?P<pk>[0-9]+)$', WarehouseDetail.as_view(), name='floatWareDetail'),

]
