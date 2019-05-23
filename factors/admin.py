from django.contrib import admin

from factors.models import Factor, FactorPayment, FactorItem, Transfer

admin.site.register(Factor)
admin.site.register(FactorItem)
admin.site.register(FactorPayment)
admin.site.register(Transfer)

