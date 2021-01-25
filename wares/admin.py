from django.contrib import admin

from wares.models import Warehouse, Ware, WareInventory, SalePriceType, SalePrice

admin.site.register(Warehouse)
admin.site.register(Ware)
admin.site.register(SalePriceType)
admin.site.register(SalePrice)
admin.site.register(WareInventory)
