from django.contrib import admin

from wares.models import Warehouse, Ware, WareBalance

admin.site.register(Warehouse)
admin.site.register(Ware)
admin.site.register(WareBalance)
