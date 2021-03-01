from django.db import models
from django_jalali.db import models as jmodels
from companies.models import FinancialYear
from distributions.models.car_model import Car
from distributions.models.distributor_model import Distributor
from distributions.models.driver_model import Driver
from helpers.models import BaseModel, EXPLANATION


class Distribution(BaseModel):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='distributions')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='distributions', blank=True)
    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT, related_name='distributions', blank=True)

    date = jmodels.jDateField()
    time = models.TimeField()

    explanation = EXPLANATION()

    class Meta(BaseModel.Meta):
        permission_basename = 'distribution'
        permissions = (
            ('get.distribution', 'مشاهده توزیع ها'),
            ('create.distribution', 'تعریف توزیع '),
            ('update.distribution', 'ویرایش توزیع '),
            ('delete.distribution', 'حذف توزیع '),
        )

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.driver = self.car.driver
            self.distributor = self.car.distributor

        super().save(*args, **kwargs)
