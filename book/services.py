from book.models import *
import datetime


def recent_messages(user: User, family: 'Family'):
    last_month = datetime.datetime.now() + datetime.timedelta(days=-30)
    last_login = user.last_login
    recent_date = last_login if last_login > last_month else last_month
    return family.posts.filter(date__gt=recent_date).exclude(read_by__contains=user)
