from django.contrib import admin

from factors.models import Receipt, Factor, FactorPayment

admin.site.register(Receipt)
admin.site.register(Factor)
admin.site.register(FactorPayment)
