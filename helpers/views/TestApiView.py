from http.client import ResponseNotReady

from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.defaultAccounts.models import DefaultAccount
from companies.models import FinancialYear


class TestApiView(APIView):
    def get(self, request):
        base_financial_year = FinancialYear.objects.get(pk=1)
        new_financial_year = FinancialYear.objects.get(pk=4)
        i = 0
        for default_account in DefaultAccount.objects.inFinancialYear(base_financial_year).filter(
                codename__icontains="imprest").all():
            default_account.pk = None
            default_account.financial_year = new_financial_year
            default_account.account_id = 1543
            default_account.save()
            i += 1

        return Response([i])
