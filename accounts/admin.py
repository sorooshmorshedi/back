from django.contrib import admin

from accounts.defaultAccounts.models import DefaultAccount
from .accounts.models import *

admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(Person)
admin.site.register(FloatAccount)
admin.site.register(DefaultAccount)
admin.site.register(AccountType)
