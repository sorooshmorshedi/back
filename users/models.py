from django.contrib.auth.models import AbstractUser, Permission
from django.db import models

from companies.models import Company, FinancialYear


class User(AbstractUser):

    active_company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='users',
                                       blank=True, null=True)
    active_financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT, related_name='users',
                                              blank=True, null=True)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def has_perm(self, perm, obj=None):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True

        (app_label, codename) = perm.split('.')
        access = Access.objects.filter(user=self, company=self.active_company,
                                       permission__codename=codename, permission__content_type__app_label=app_label)
        if access.count() == 1:
            return True
        return False


class Access(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, related_name='accesses')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='accesses')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='accesses')

    class Meta:
        unique_together = ('permission', 'company', 'user')

