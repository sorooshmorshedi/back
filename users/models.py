from django.contrib.auth.models import AbstractUser, Permission
from django.db import models

from companies.models import Company, FinancialYear


class User(AbstractUser):
    active_company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='usersActiveCompany',
                                       blank=True, null=True)
    active_financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT, related_name='users',
                                              blank=True, null=True)

    phone = models.CharField(max_length=11, default="", blank=True)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def has_perm(self, perm, company=None):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True

        if not company:
            company = self.active_company

        return super(User, self).has_perm(perm, company)
