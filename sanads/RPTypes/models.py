from django.db import models

from accounts.accounts.models import Account

USAGES = (
    ('receive', 'receive'),
    ('payment', 'payment'),
    ('both', 'both')
)


class RPType(models.Model):
    name = models.CharField(unique=True, max_length=150)
    exp = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='RPType',)
    usage = models.CharField(choices=USAGES, max_length=20)


