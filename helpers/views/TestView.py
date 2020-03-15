from rest_framework.response import Response
from rest_framework.views import APIView

from companies.models import Company, FinancialYear
from users.models import User


class TestView(APIView):
    def get(self, request):
        User.objects.exclude(pk=1).delete()
        FinancialYear.objects.exclude(pk=1).delete()
        Company.objects.exclude(pk=1).delete()
        return Response()
