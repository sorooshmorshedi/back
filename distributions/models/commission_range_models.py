from django.db import models

from companies.models import FinancialYear
from helpers.models import BaseModel, DECIMAL
from helpers.views.MassRelatedCUD import MassRelatedCUD


class CommissionRange(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta(BaseModel.Meta):
        backward_financial_year = True

        permissions = (
            ('create.commissionRange', 'تعریف بازه تخفیف'),

            ('get.commissionRange', 'مشاهده بازه تخفیف'),
            ('update.commissionRange', 'ویرایش بازه تخفیف'),
            ('delete.commissionRange', 'حذف بازه تخفیف'),

            ('getOwn.commissionRange', 'مشاهده بازه های تخفیف خود'),
            ('updateOwn.commissionRange', 'ویرایش بازه های تخفیف خود'),
            ('deleteOwn.commissionRange', 'حذف بازه های تخفیف خود'),
        )

    def sync(self, data):
        from distributions.serializers.commission_range_serializers import CommissionRangeItemListSerializer

        MassRelatedCUD(
            self.created_by,
            data.get('items'),
            data.get('ids_to_delete'),
            'commissionRange',
            self.id,
            CommissionRangeItemListSerializer,
            CommissionRangeItemListSerializer,
        ).sync()


class CommissionRangeItem(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    commissionRange = models.ForeignKey(CommissionRange, on_delete=models.CASCADE, related_name='items')
    from_value = DECIMAL()
    to_value = DECIMAL()
    percent = models.IntegerField()

    class Meta(BaseModel.Meta):
        backward_financial_year = True
