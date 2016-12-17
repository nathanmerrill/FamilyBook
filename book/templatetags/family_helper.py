from django import template
from book.models import *
from django.template.defaultfilters import timesince

register = template.Library()


@register.filter("timesince_short", is_safe=False)
def timesince_short(value, arg=None):
    if not value:
        return ''
    try:
        return timesince(value, arg).split(",")[0]
    except (ValueError, TypeError):
        return


@register.filter("error_list", is_safe=False)
def error_list(request):
    if 'errors' not in request.session:
        return ''
    errors = request.session['errors']
    ret = ",".join('"'+error+'"' for error in errors)
    del request.session['errors']
    return ret


def friendly_date(date: datetime):
    if not date:
        return ''
    today = datetime.datetime.now().date()
    difference = today-date.date()
    if difference < 0:
        if difference == -1:
            return "Yesterday"
    elif difference > 0:
        pass
    else:
        return "Today"



