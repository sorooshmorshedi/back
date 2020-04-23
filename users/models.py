from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

from companies.models import Company, FinancialYear


class Role(models.Model):
    company = models.ForeignKey(Company, related_name='roles', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')


class User(AbstractUser):
    active_company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='usersActiveCompany',
                                       blank=True, null=True)
    active_financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT, related_name='users',
                                              blank=True, null=True)

    phone = models.CharField(max_length=11, default="", blank=True)

    roles = models.ManyToManyField(Role, related_name='users')

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'

    def has_perm(self, permission_codename, company=None):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True

        if not company:
            company = self.active_company

        return self.roles.filter(company=company, permissions__codename=permission_codename).exists()
