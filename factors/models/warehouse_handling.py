from django.db import models
from django_jalali.db import models as jmodels

from companies.models import FinancialYear
from factors.models.adjustment import Adjustment
from helpers.models import BaseModel, EXPLANATION, DECIMAL
from wares.models import Warehouse, Ware


class WarehouseHandling(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='warehouseHandlings')
    code = models.IntegerField(blank=True, null=True)

    start_date = jmodels.jDateField()
    counting_date = jmodels.jDateField()
    submit_date = jmodels.jDateField()
    submit_time = models.TimeField()
    handler = models.CharField(max_length=200)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='warehouseHandlings')
    ware_status = models.CharField(max_length=20)
    explanation = EXPLANATION()

    is_defined = models.BooleanField(default=False)
    inputAdjustment = models.ForeignKey(Adjustment, on_delete=models.PROTECT, related_name='warehouseHandlingAsInput',
                                        blank=True, null=True)
    outputAdjustment = models.ForeignKey(Adjustment, on_delete=models.PROTECT, related_name='warehouseHandlingAsOutput',
                                         blank=True, null=True)

    class Meta(BaseModel.Meta):
        permission_basename = 'warehouseHandling'
        permissions = (
            ('get.warehouseHandling', 'مشاهده انبار گردانی'),
            ('create.warehouseHandling', 'تعریف انبار گردانی'),
            ('update.warehouseHandling', 'ویرایش انبار گردانی'),
            ('delete.warehouseHandling', 'حذف انبار گردانی'),
        )


class WarehouseHandlingItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, related_name='warehouseHandlingItems')
    warehouseHandling = models.ForeignKey(WarehouseHandling, on_delete=models.CASCADE, related_name='items')
    ware = models.ForeignKey(Ware, on_delete=models.PROTECT, related_name='warehouseHandlingItems')
    warehouse_remain = DECIMAL(null=True, default=None)
    system_remain = DECIMAL(null=True, default=None)

    order = models.IntegerField(default=0)

    explanation = EXPLANATION()

    @property
    def contradiction(self):
        if self.warehouse_remain is not None:
            return self.warehouse_remain - self.system_remain
        return None