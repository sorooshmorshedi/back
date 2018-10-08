from django.contrib import admin

from sanads.sanads.models import *
from sanads.transactions.models import Transaction

admin.site.register(Sanad)
admin.site.register(SanadItem)
admin.site.register(Transaction)
