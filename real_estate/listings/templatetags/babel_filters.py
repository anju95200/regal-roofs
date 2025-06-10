from babel.numbers import format_currency
from django import template

register = template.Library()

@register.filter
def inr_currency(value):
    try:
        formatted_value = format_currency(value, 'INR', locale='en_IN')
        return formatted_value.split('.')[0]
    except (ValueError, TypeError):
        return value
