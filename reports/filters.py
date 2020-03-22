from django.db.models.query_utils import Q

from helpers.functions import get_current_user


def get_account_sanad_items_filter(request) -> Q:
    data = request.GET

    filters = Q()
    if 'from_date' in data:
        filters &= Q(sanadItems__sanad__date__gte=data['from_date'])
    if 'to_date' in data:
        filters &= Q(sanadItems__sanad__date__lte=data['to_date'])
    if 'from_code' in data:
        filters &= Q(sanadItems__sanad__code__gte=data['from_code'])
    if 'to_code' in data:
        filters &= Q(sanadItems__sanad__code__lte=data['to_code'])
    if 'codes' in data:
        filters &= Q(sanadItems__sanad__code__in=data['codes'])
    if data.get('skip_closing_sanad', False) == 'true':
        financial_year = get_current_user().active_financial_year
        closing_sanad = financial_year.closing_sanad
        if closing_sanad:
            filters &= ~Q(sanadItems__sanad=closing_sanad)

    return filters
