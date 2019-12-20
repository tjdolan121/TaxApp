from django import template
from ..views import get_total_shares
import datetime

register = template.Library()


@register.filter(name="get_total_shares")
def show_total_shares(holding):
    return get_total_shares(holding)


@register.filter(name="date_only")
def date_only(date_obj):
    d = datetime.datetime.strptime(str(date_obj), '%Y-%m-%d %H:%M:%S')
    d = d.strftime('%m/%d/%Y')
    return d
