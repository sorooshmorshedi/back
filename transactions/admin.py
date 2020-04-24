from django.contrib import admin

from transactions.models import Transaction, TransactionItem

admin.site.register(Transaction)
admin.site.register(TransactionItem)
