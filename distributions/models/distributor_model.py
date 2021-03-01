from django.db import models
from companies.models import FinancialYear
from helpers.models import BaseModel
from users.models import User


class Distributor(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='distributors')

    class Meta(BaseModel.Meta):
        unique_together = (('financial_year', 'user'), )
        backward_financial_year = True
        permission_basename = 'distributor'
        permissions = (
            ('get.distributor', 'مشاهده موزع ها'),
            ('create.distributor', 'تعریف موزع'),
            ('update.distributor', 'ویرایش موزع'),
            ('delete.distributor', 'حذف موزع'),
        )
