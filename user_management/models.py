from django.contrib.auth.models import AbstractUser, Permission
from django.db import models

from companies.models import Company, FinancialYear


class User(AbstractUser):

    active_company = models.OneToOneField(Company, on_delete=models.PROTECT, related_name='users',
                                          blank=True, null=True)
    active_financial_year = models.OneToOneField(FinancialYear, on_delete=models.PROTECT, related_name='users',
                                                 blank=True, null=True)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def has_perm(self, perm, obj=None):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True
        access = Access.objects.filter(company=self.active_company)
        if access.count() == 1:
            return True
        return False


class Access(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, related_name='accesses')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='accesses')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='accesses')

    class Meta:
        unique_together = ('permission', 'company', 'user')

