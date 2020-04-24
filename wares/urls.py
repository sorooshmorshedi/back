from django.conf.urls import url

from wares.views import WareLevelListCreate, WareLevelDetail, WareListCreate, WareDetail, WarehouseListCreate, \
    UnitListCreate, UnitDetail, WarehouseDetail, WareInventoryView

urlpatterns = [
    url(r'^wareLevels$', WareLevelListCreate.as_view(), name='Wares'),
    url(r'^wareLevels/(?P<pk>[0-9]+)$', WareLevelDetail.as_view(), name='WareDetail'),

    url(r'^wares$', WareListCreate.as_view(), name='Wares'),
    url(r'^wares/(?P<pk>[0-9]+)$', WareDetail.as_view(), name='WareDetail'),

    url(r'^units$', UnitListCreate.as_view(), name='units'),
    url(r'^units/(?P<pk>[0-9]+)$', UnitDetail.as_view(), name='unitDetail'),

    url(r'^warehouses$', WarehouseListCreate.as_view(), name='warehouse'),
    url(r'^warehouses/(?P<pk>[0-9]+)$', WarehouseDetail.as_view(), name='floatWareDetail'),

    url(r'^inventory/forWare$', WareInventoryView.as_view(), name=''),

]
