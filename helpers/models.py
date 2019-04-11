from django.db import models


class BaseManager(models.Manager):
    def inFinancialYear(self, user):
        return super().get_queryset().filter(financial_year=user.active_financial_year)


class BaseModel(models.Model):

    class Meta:
        abstract = True
        default_permissions = ()

    objects = BaseManager()


