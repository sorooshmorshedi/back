from django.contrib import admin

from factors.models import Factor, FactorPayment, FactorItem, Transfer, Expense, Adjustment

admin.site.register(Factor)
admin.site.register(FactorItem)
admin.site.register(FactorPayment)
admin.site.register(Transfer)
admin.site.register(Adjustment)
admin.site.register(Expense)

