import os
from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.accounts.models import Account
from accounts.defaultAccounts.models import DefaultAccount
from companies.models import FinancialYear


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        for financial_year in FinancialYear.objects.all():
            print(financial_year)
            parents = [
                DefaultAccount.get("realBuyerParent", financial_year).account,
                DefaultAccount.get("legalBuyerParent", financial_year).account,
                DefaultAccount.get("contractorBuyerParent", financial_year).account,
                DefaultAccount.get("otherBuyerParent", financial_year).account,
                DefaultAccount.get("realSellerParent", financial_year).account,
                DefaultAccount.get("legalSellerParent", financial_year).account,
                DefaultAccount.get("contractorSellerParent", financial_year).account,
                DefaultAccount.get("otherSellerParent", financial_year).account,
            ]
            Account.objects.filter(parent__in=parents).update(account_type=Account.PERSON)

            Account.objects.filter(parent=DefaultAccount.get("bankParent", financial_year).account).update(
                account_type=Account.BANK
            )
