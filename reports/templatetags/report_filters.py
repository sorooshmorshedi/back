from django import template

register = template.Library()


@register.filter(is_safe=True)
def money(value):
    return 'ha'
