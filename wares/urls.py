from django.conf.urls import url

from wares.views import WareListCreateView, WareDetailView, WarehouseListCreate, UnitListCreate, UnitDetail, WarehouseDetail, \
    SortInventoryView, SalePriceTypeListCreate, SalePriceTypeDetail, ChangeSalePricesView

urlpatterns = [
    url(r'^wares$', WareListCreateView.as_view(), name='Wares'),
    url(r'^wares/(?P<pk>[0-9]+)$', WareDetailView.as_view(), name='WareDetail'),

    url(r'^units$', UnitListCreate.as_view(), name='units'),
    url(r'^units/(?P<pk>[0-9]+)$', UnitDetail.as_view(), name='unitDetail'),

    url(r'^salePriceTypes$', SalePriceTypeListCreate.as_view(), name='salePriceTypes'),
    url(r'^salePriceTypes/(?P<pk>[0-9]+)$', SalePriceTypeDetail.as_view(), name='salePriceTypesDetail'),

    url(r'^warehouses$', WarehouseListCreate.as_view(), name='warehouse'),
    url(r'^warehouses/(?P<pk>[0-9]+)$', WarehouseDetail.as_view(), name='floatWareDetail'),

    url(r'^sortInventory$', SortInventoryView.as_view(), name='sortInventory'),

    url(r'^changeSalePrices$', ChangeSalePricesView.as_view(), name='changeSalePrice'),
]
