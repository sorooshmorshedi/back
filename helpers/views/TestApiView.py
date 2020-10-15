from django.db import connection
from django.db.models.aggregates import Sum
from django.db.models.functions.comparison import Coalesce
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.accounts.models import Account


class TestApiView(APIView):
    def get(self, request):
        data = []
        accounts = Account.objects.prefetch_related(
            'sanadItems',
            'children__sanadItems',
            'children__children__sanadItems',
            'children__children__children__sanadItems',
        ).annotate(
            bed_sum=Coalesce(
                Sum('sanadItems__bed'),
                Coalesce(
                    Sum('children__children__sanadItems__bed'),
                    Coalesce(
                        Sum('children__children__sanadItems__bed'),
                        Coalesce(Sum('children__children__children__sanadItems__bed'), 0)
                    )
                )
            )
        ).all()
        data.append([accounts.count()])
        for account in accounts:
            if account.bed_sum == 0:
                continue
            data.append(
                [
                    account.id,
                    account.code,
                    account.bed_sum,
                ]
            )

        print(connection.queries)
        return Response(data)
