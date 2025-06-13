from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def smart_date(value):
    if not value:
        return ""

    now = timezone.now()
    today = now.date()
    date = value.date()

    delta = today - date

    if delta.days == 0:
        return "TODAY"
    elif delta.days == 1:
        return "YESTERDAY"
    elif 1 < delta.days <= 30:
        return f"{delta.days} DAYS AGO"
    elif date.year == today.year:
        return value.strftime("%b %d")
    else:
        return value.strftime("%b %d %Y")


@register.filter
def yes_no(value):
    if value:
        return "Yes"
    return "No"

# Yellow Star
@register.filter
def times(number):
    return range(number)


# Grey Star
@register.filter
def remaining_times(number, total):
    try:
        return int(total) - int(number)
    except:
        return 0
    
    
@register.filter
def mask_email(email):
    local, domain = email.split('@')
    if len(local) <= 5:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    else:
        masked_local = local[:3] + '*' * (len(local) - 5) + local[-2:]
    return masked_local + '@' + domain


@register.filter
def mask_phone(phone):
    phone = str(phone)
    if len(phone) == 10:
        return phone[:3] + '*' * 5 + phone[-2:]
    return phone
