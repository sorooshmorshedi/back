from django import template
from reports.models import ExportVerifier

register = template.Library()


@register.inclusion_tag('reports/export_verifiers.html')
def show_verifiers(form, user):
    verifiers = ExportVerifier.objects.filter(form=form)
    count = len(verifiers)
    if count == 1:
        col_number = 12
    elif count == 2:
        col_number = 6
    else:
        col_number = 4
    return {
        'verifiers': verifiers,
        'col_number': col_number
    }
