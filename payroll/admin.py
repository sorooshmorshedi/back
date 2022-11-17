
from django.contrib import admin

from payroll.models import Workshop, Personnel, PersonnelFamily, WorkshopPersonnel, ContractRow, Contract, HRLetter, \
    LeaveOrAbsence, ListOfPay, ListOfPayItem, WorkshopTaxRow, WorkshopTax, Loan, OptionalDeduction, LoanItem


admin.site.register(Workshop)
admin.site.register(WorkshopTax)
admin.site.register(WorkshopTaxRow)
admin.site.register(Personnel)
admin.site.register(PersonnelFamily)
admin.site.register(WorkshopPersonnel)
admin.site.register(ContractRow)
admin.site.register(Contract)
admin.site.register(HRLetter)
admin.site.register(LeaveOrAbsence)
admin.site.register(ListOfPay)
admin.site.register(ListOfPayItem)
admin.site.register(Loan)
admin.site.register(OptionalDeduction)
admin.site.register(LoanItem)
