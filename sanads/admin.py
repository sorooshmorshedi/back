from django.contrib import admin

from sanads.sanads.models import *
from sanads.transactions.models import Transaction, TransactionItem

admin.site.register(Sanad)
admin.site.register(SanadItem)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
