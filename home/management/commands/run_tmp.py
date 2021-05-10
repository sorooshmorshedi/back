from django.core.management.base import BaseCommand
from companies.models import Company, CompanyUser
from factors.factor_sanad import FactorSanad
from factors.models import Factor
from helpers.test import set_user


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        for company in Company.objects.all():
            print("Company #{}".format(company.id))
            superuser = company.superuser

            set_user(superuser)

            if not company.created_by:
                company.created_by = superuser
            company.modules = superuser.modules
            company.save()

            financial_years = company.financial_years.all()
            users = list(superuser.users.all())
            users.append(superuser)
            for user in users:
                print(" - User #{}".format(user.id))
                obj, created = CompanyUser.objects.get_or_create(
                    company=company,
                    user=user,
                )
                obj.financialYears.set(financial_years)
                obj.roles.set(user.roles.all())
                print(' -- ', obj, created)

    def update_all_factors_sanads(self):
        i = 0
        qs = Factor.objects.filter(is_definite=True)
        count = qs.count()
        for factor in qs:
            print("{}/{} : {}".format(count, i + 1, factor.id))
            set_user(factor.created_by)
            try:
                FactorSanad(factor).update(True)
            except Exception as e:
                print(e)
            i += 1
