from django.contrib import admin

from factors.models import Factor, FactorPayment, FactorItem

admin.site.register(Factor)
admin.site.register(FactorItem)
admin.site.register(FactorPayment)

