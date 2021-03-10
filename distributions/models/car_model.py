from django.db import models
from companies.models import FinancialYear
from distributions.models.distributor_model import Distributor
from distributions.models.driver_model import Driver
from helpers.models import BaseModel, EXPLANATION


class Car(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    car_number = models.CharField(max_length=11)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='cars')
    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT, related_name='cars')
    explanation = EXPLANATION()

    class Meta(BaseModel.Meta):
        backward_financial_year = True
        permission_basename = 'car'
        permissions = (
            ('create.car', 'تعریف ماشین '),

            ('get.car', 'مشاهده ماشین ها'),
            ('update.car', 'ویرایش ماشین '),
            ('delete.car', 'حذف ماشین '),

            ('getOwn.car', 'مشاهده ماشین های خود'),
            ('updateOwn.car', 'ویرایش ماشین های خود'),
            ('deleteOwn.car', 'حذف ماشین های خود'),
        )
