from django.contrib import admin
from .models import *

admin.site.register(Warehouse)
admin.site.register(Ware)
admin.site.register(WarehouseInventory)
