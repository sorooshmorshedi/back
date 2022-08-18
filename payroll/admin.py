
from django.contrib import admin

from payroll.models import Workshop, Personnel, PersonnelFamily, WorkshopPersonnel, ContractRow, Contract, HRLetter

admin.site.register(Workshop)
admin.site.register(Personnel)
admin.site.register(PersonnelFamily)
admin.site.register(WorkshopPersonnel)
admin.site.register(ContractRow)
admin.site.register(Contract)
admin.site.register(HRLetter)
