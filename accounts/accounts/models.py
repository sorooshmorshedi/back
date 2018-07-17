from django.db import models

from accounts.costCenter.models import CostCenter, CostCenterGroup

ACCOUNT_LEVELS = (
    (0, 'group'),
    (1, 'kol'),
    (2, 'moein'),
    (3, 'tafzili'),
)


class FloatAccountGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return str(self.pk) + ' - ' + self.name


class FloatAccount(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    max_bed = models.CharField(max_length=20, blank=True, null=True)
    max_bes = models.CharField(max_length=20, blank=True, null=True)
    max_bed_with_sanad = models.CharField(max_length=20, blank=True, null=True)
    max_bes_with_sanad = models.CharField(max_length=20, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.PROTECT, related_name='floatAccounts')

    class Meta:
        default_permissions = ()


class AccountType(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=3, choices=(('BED', 'bedehkar'),('BES', 'bestankar')))

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name


class IndependentAccount(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    max_bed = models.IntegerField(blank=True, null=True)
    max_bes = models.IntegerField( blank=True, null=True)
    max_bed_with_sanad = models.IntegerField(blank=True, null=True)
    max_bes_with_sanad = models.IntegerField(blank=True, null=True)

    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    level = models.IntegerField(choices=ACCOUNT_LEVELS)

    type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, related_name='accounts', blank=True, null=True)
    costCenterGroup = models.ForeignKey(CostCenterGroup, on_delete=models.PROTECT, related_name='accounts', blank=True, null=True)
    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.PROTECT, related_name='accounts', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)

    permissions = (
        ('get_account', 'Can get accounts')
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]





