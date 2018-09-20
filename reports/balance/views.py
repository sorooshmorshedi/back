from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.accounts.models import Account
from reports.balance.serializers import AccountBalanceSerializer


@api_view(['get'])
def accountBalanceView(request):

    data = request.GET

    dateFilter = Q()
    if 'from_date' in data:
        dateFilter &= Q(sanadItems__sanad__date__gte=data['from_date'])
    if 'to_date' in data:
        dateFilter &= Q(sanadItems__sanad__date__lte=data['to_date'])
    if 'from_code' in data:
        dateFilter &= Q(sanadItems__sanad__code__gte=data['from_code'])
    if 'to_code' in data:
        dateFilter &= Q(sanadItems__sanad__code__lte=data['to_code'])
    if 'codes' in data:
        dateFilter &= Q(sanadItems__sanad__code__in=data['codes'])

    accounts = Account.objects\
        .annotate(bed_sum=Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bed') & dateFilter), 0))\
        .annotate(bes_sum=Coalesce(Sum('sanadItems__value', filter=Q(sanadItems__valueType='bes') & dateFilter), 0)) \
        .order_by('code')

    for account in accounts:
        if account.level != 3:
            for acc in accounts:
                if acc == account or acc.level != 3:
                    continue
                if acc.code.find(account.code) == 0:
                    account.bed_sum += acc.bed_sum
                    account.bes_sum += acc.bes_sum

        remain = account.bed_sum - account.bes_sum
        if remain > 0:
            account.bed_remain = remain
            account.bes_remain = 0
        else:
            account.bes_remain = -remain
            account.bed_remain = 0

    return Response(AccountBalanceSerializer(accounts, many=True).data)
