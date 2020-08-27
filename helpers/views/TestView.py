from django.db.models.aggregates import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.accounts.models import Account


class TestView(APIView):
    def get(self, request):
        c = Account.objects.filter(code='101010002').delete()
        return Response([c])
