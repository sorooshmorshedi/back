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


@register.filter
def get_item(obj, key):
    value = rgetattr(obj, key)

    if value is None:
        value = '-'

    return value
