from django.db import models
from django_jalali.db import models as jmodels

from companies.models import FinancialYear
from factors.models.factor import Factor
from helpers.functions import get_current_user
from helpers.models import BaseModel, EXPLANATION, DefinableMixin, LockableMixin
from sanads.models import Sanad


class Adjustment(BaseModel, DefinableMixin, LockableMixin):
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
            ('define.adjustment', 'قطعی کردن تعدیل '),
            ('lock.adjustment', 'قفل کردن تعدیل '),

            ('getOwn.adjustment', 'مشاهده تعدیل های خود'),
            ('updateOwn.adjustment', 'ویرایش تعدیل های خود'),
            ('deleteOwn.adjustment', 'حذف تعدیل های خود'),
            ('defineOwn.adjustment', 'قطعی کردن تعدیل های خود'),
            ('lockOwn.adjustment', 'قفل کردن تعدیل های خود')
        )

    def define(self, date=None):
        from factors.views.definite_factor import DefiniteFactor
        from factors.adjustment_sanad import AdjustmentSanad
        from django.utils.timezone import now

        if not self.is_defined:
            DefiniteFactor.updateFactorInventory(self.factor)
            AdjustmentSanad(self).update()
            self.is_defined = True
            self.defined_by = get_current_user()
            self.definition_date = date or now()
            self.save()
