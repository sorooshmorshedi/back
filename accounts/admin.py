from django.contrib import admin

from accounts.defaultAccounts.models import DefaultAccount
from .accounts.models import *


class FloatAccountRelationInline(admin.TabularInline):
    model = FloatAccountRelation
    extra = 1


class FloatAccountAdmin(admin.ModelAdmin):
    inlines = (FloatAccountRelationInline,)


class FloatAccountGroupAdmin(admin.ModelAdmin):
    inlines = (FloatAccountRelationInline,)


admin.site.register(Account)
admin.site.register(FloatAccount, FloatAccountAdmin)
admin.site.register(FloatAccountGroup, FloatAccountGroupAdmin)
admin.site.register(DefaultAccount)
admin.site.register(AccountType)
