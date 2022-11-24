from django.contrib import admin

from contracting.models import Tender, Contract, Statement, Supplement

admin.site.register(Tender)
admin.site.register(Contract)
admin.site.register(Statement)
admin.site.register(Supplement)


