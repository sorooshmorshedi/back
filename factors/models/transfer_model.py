from django.db import models
from django_jalali.db import models as jmodels

from companies.models import FinancialYear
from factors.models.factor import Factor
from helpers.models import BaseModel, DefinableMixin


class Transfer(BaseModel, DefinableMixin):
    code = models.IntegerField()
    date = jmodels.jDateField()
    time = models.TimeField()

    input_factor = models.ForeignKey(Factor, on_delete=models.PROTECT, related_name='input_transfer')
    output_factor = models.ForeignKey(Factor, on_delete=models.PROTECT, related_name='output_transfer')
    explanation = models.CharField(max_length=255, blank=True)

    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='transfers')

    class Meta(BaseModel.Meta):
        permission_basename = 'transfer'
        permissions = (
            ('get.transfer', 'مشاهده انتقال'),
            ('create.transfer', 'تعریف انتقال'),
            ('update.transfer', 'ویرایش انتقال'),
            ('delete.transfer', 'حذف انتقال'),
            ('define.transfer', 'قطعی کردن انتقال'),

            ('getOwn.transfer', 'مشاهده انتقال های خود'),
            ('updateOwn.transfer', 'ویرایش انتقال های خود'),
            ('deleteOwn.transfer', 'حذف انتقال های خود'),
            ('defineOwn.transfer', 'قطعی کردن انتقال های خود'),
        )
