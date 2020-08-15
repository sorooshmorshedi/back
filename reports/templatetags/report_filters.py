from django import template

register = template.Library()


@register.filter(is_safe=True)
def money(value):
    try:
        str_value = '{:,}'.format(value)
    except ValueError:
        return value
    if '.' in str_value:
        str_value = str_value.strip('0')
    str_value = str_value.strip('.')
    return str_value


@register.simple_tag
def colspan(initial_count, *args):
    count = initial_count
    for arg in args:
        if arg:
            count += 1
    return count
