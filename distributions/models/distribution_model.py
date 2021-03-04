import datetime

import jdatetime
from django.db import models
from django_jalali.db import models as jmodels
from companies.models import FinancialYear
from distributions.models.car_model import Car
from distributions.models.distributor_model import Distributor
from distributions.models.driver_model import Driver
from helpers.functions import get_current_user
from helpers.models import BaseModel, EXPLANATION, LocalIdMixin


class Distribution(BaseModel, LocalIdMixin):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)

    code = models.IntegerField()
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

    def sync(self, previous_factors=()):
        new_factors = self.factors.all()

        for factor in new_factors:
            if factor not in previous_factors:
                print('n', factor.id)
                factor.is_loaded = True
                factor.loaded_by = get_current_user()
                factor.loading_date = datetime.datetime.combine(self.date.togregorian(), self.time)
                factor.save()

        for factor in previous_factors:
            if factor not in new_factors:
                print('p', factor.id)
                factor.is_loaded = False
                factor.loaded_by = None
                factor.loading_date = None
                factor.save()

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.driver = self.car.driver
            self.distributor = self.car.distributor

        super().save(*args, **kwargs)
