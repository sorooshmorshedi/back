from rest_framework.response import Response
from rest_framework.views import APIView

from _dashtbashi.models import Lading


class TestApiView(APIView):
    def get(self, request):
        for lading in Lading.objects.filter(financial_year_id=4).order_by('pk'):
            lading.save()

        return Response([])
