from django.db import models

from accounts.defaultAccounts.models import DefaultAccount
from companies.models import FinancialYear
from helpers.models import BaseModel
from users.models import User


class Distributor(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='distributors')
    defaultAccounts = models.ManyToManyField(DefaultAccount, related_name='distributors')

    class Meta(BaseModel.Meta):
        unique_together = (('financial_year', 'user'), )
        backward_financial_year = True
        permission_basename = 'distributor'
        permissions = (
            ('create.distributor', 'تعریف موزع'),

            ('get.distributor', 'مشاهده موزع ها'),
            ('update.distributor', 'ویرایش موزع'),
            ('delete.distributor', 'حذف موزع'),

            ('getOwn.distributor', 'مشاهده موزع های خود'),
            ('updateOwn.distributor', 'ویرایش موزع های خود'),
            ('deleteOwn.distributor', 'حذف موزع های خود'),
        )
