from django.db import models
from companies.models import FinancialYear
from helpers.models import BaseModel
from users.models import User


class Driver(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='drivers')

    class Meta(BaseModel.Meta):
        unique_together = (('financial_year', 'user'), )
        backward_financial_year = True
        permission_basename = 'driver'
        permissions = (
            ('get.driver', 'مشاهده راننده ها'),
            ('create.driver', 'تعریف راننده '),
            ('update.driver', 'ویرایش راننده '),
            ('delete.driver', 'حذف راننده '),
        )
