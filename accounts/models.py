from django.db import models


class CostCenterGroup(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()


class CostCenter(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(CostCenterGroup, on_delete=models.CASCADE, related_name='costCenters')

    permissions = (
        ('get_costCenter', 'Can get cost centers')
    )


class FloatAccountGroup(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()


class FloatAccount(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(FloatAccountGroup, on_delete=models.CASCADE, related_name='floatAccounts')

    class Meta:
        default_permissions = ()


class AccountType(models.Model):
    name = models.CharField(max_length=100)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=3, choices=(('BED', 'bedehkar'),('BES', 'bestankar')))

    class Meta:
        default_permissions = ()


class Account(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    is_disabled = models.BooleanField(default=False)

    max_bed = models.CharField(max_length=20, blank=True, null=True)
    max_bes = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    type = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name='accounts')
    costCenter = models.ForeignKey(CostCenter, on_delete=models.CASCADE, related_name='accounts', blank=True, null=True)
    floatAccountGroup = models.ForeignKey(FloatAccountGroup, on_delete=models.CASCADE, related_name='accounts', blank=True, null=True)

    permissions = (
        ('get_account', 'Can get accounts')
    )



