from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def querystring_without_page(context, page_num):
    request = context['request']
    query_dict = request.GET.copy()
    if 'page' in query_dict:
        del query_dict['page']  # Remove the 'page' parameter
    query_dict['page'] = page_num  # Add the new page number
    return query_dict.urlencode()