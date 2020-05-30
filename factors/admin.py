from django.contrib import admin

from factors.models import Factor, FactorPayment, FactorItem, Transfer, Expense

admin.site.register(Factor)
admin.site.register(FactorItem)
admin.site.register(FactorPayment)
admin.site.register(Transfer)
admin.site.register(Expense)

