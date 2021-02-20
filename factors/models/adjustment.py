from django.db import models
from django_jalali.db import models as jmodels

from companies.models import FinancialYear
from factors.models.factor import Factor
from helpers.models import BaseModel, EXPLANATION
from sanads.models import Sanad


class Adjustment(BaseModel):
    code = models.IntegerField()
    date = jmodels.jDateField()
    time = models.TimeField()

    type = models.CharField(max_length=2, choices=Factor.ADJUSTMENT_TYPES)
    factor = models.ForeignKey(Factor, on_delete=models.PROTECT, related_name='adjustment')
    sanad = models.OneToOneField(Sanad, on_delete=models.PROTECT, related_name='adjustment', null=True)
    explanation = EXPLANATION()

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        permission_basename = 'adjustment'
        permissions = (
            ('get.adjustment', 'مشاهده تعدیل '),
            ('create.adjustment', 'تعریف تعدیل '),
            ('update.adjustment', 'ویرایش تعدیل '),
            ('delete.adjustment', 'حذف تعدیل '),

            ('getOwn.adjustment', 'مشاهده تعدیل های خود'),
            ('updateOwn.adjustment', 'ویرایش تعدیل های خود'),
            ('deleteOwn.adjustment', 'حذف تعدیل های خود'),
        )