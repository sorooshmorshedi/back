from django.db import models
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('backward_financial_year',)


class BaseManager(models.Manager):

    def inFinancialYear(self, financial_year=None):
        from helpers.functions import get_current_user
        user = get_current_user()

        if not financial_year:
            financial_year = user.active_financial_year

        qs = super().get_queryset()
        if self.model._meta.backward_financial_year:
            return qs.filter(financial_year__id__lte=financial_year.id)
        else:
            return qs.filter(financial_year=financial_year.id)


class BaseModel(models.Model):
    class Meta:
        abstract = True
        default_permissions = ()
        ordering = ['pk']
        backward_financial_year = False

    objects = BaseManager()
