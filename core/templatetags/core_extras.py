from datetime import date

from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('generic/copyright.html')
def copyright_year():
    start_year = settings.START_PUBLISH_YEAR
    current_year = date.today().year
    ret = '{} - {}'.format(start_year, current_year) if start_year < current_year else current_year
    return {
        'year': ret
    }
