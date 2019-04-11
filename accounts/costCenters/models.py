from django.db import models
from helpers.models import BaseModel


class CostCenterGroup(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'گروه مرکز هزینه'

    def __str__(self):
        return self.name


class CostCenter(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    explanation = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(CostCenterGroup, on_delete=models.PROTECT, related_name='costCenters')

    class Meta(BaseModel.Meta):
        verbose_name = 'مرکز هزینه'

    def __str__(self):
        return self.name

