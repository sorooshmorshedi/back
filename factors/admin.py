from django.contrib import admin

from factors.models import Factor, Expense, Adjustment
from factors.models.transfer_model import Transfer
from factors.models.warehouse_handling import WarehouseHandling, WarehouseHandlingItem
from factors.models.factor import FactorPayment, FactorItem

admin.site.register(Factor)
admin.site.register(FactorItem)
admin.site.register(FactorPayment)
admin.site.register(Transfer)
admin.site.register(Adjustment)
admin.site.register(Expense)
admin.site.register(WarehouseHandling)
admin.site.register(WarehouseHandlingItem)

