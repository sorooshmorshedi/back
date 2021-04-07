from django import template

from factors.models import Factor
from helpers.functions import add_separator, get_object_account_names, rgetattr

register = template.Library()


@register.filter(is_safe=True)
def money(value):
    return add_separator(value)


@register.simple_tag
def colspan(initial_count, *args):
    count = initial_count
    for arg in args:
        if arg:
            count += 1
    return count


@register.simple_tag
def factor_title(factor: Factor):
    return "{}فاکتور {}".format("پیش " if not factor.is_definite else "", Factor.get_type_label(factor.type))


@register.simple_tag
def account_name(obj):
    return get_object_account_names(obj)


@register.simple_tag
def get_value(obj, key, headers):
    if isinstance(obj, list):
        value = obj[key]
    else:
        value = rgetattr(obj, key)

    if value is None:
        return '-'

    header = [header for header in headers if header['value'] == key][0]
    value_type = header.get('type', None)

    if value_type == 'numeric':
        return add_separator(value)
    elif value_type == 'select':
        return [item['text'] for item in header['items'] if item['value'] == value][0]
    elif value_type == 'boolean':
        return '&#10004;' if value else '&#10006;'

    return value


@register.simple_tag
def get_ordered_items(obj):
    return obj.items.order_by('order')
