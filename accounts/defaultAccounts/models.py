from django.db import models

from accounts.accounts.models import Account

USAGES = (
    ('receive', 'receive'),
    ('payment', 'payment'),
    ('both', 'both')
)


class DefaultAccount(models.Model):
    name = models.CharField(unique=True, max_length=150)
    explanation = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='defaultAccount')
    usage = models.CharField(choices=USAGES, max_length=20)

    programingName = models.CharField(unique=True, max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


def getDA(pn):
    return DefaultAccount.objects.get(programingName=pn)



