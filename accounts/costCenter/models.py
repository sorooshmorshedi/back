from django.db import models


class CostCenterGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name


class CostCenter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(CostCenterGroup, on_delete=models.PROTECT, related_name='costCenters')

    permissions = (
        ('get_costCenter', 'Can get cost centers')
    )

    def __str__(self):
        return self.name;

