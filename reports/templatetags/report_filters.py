from django import template

register = template.Library()


@register.filter(is_safe=True)
def money(value):
    try:
        return '{:,}'.format(value)
    except ValueError:
        return value
