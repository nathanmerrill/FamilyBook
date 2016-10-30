from django.http import Http404
from django.http import HttpRequest

from book import models
from django.shortcuts import get_object_or_404


class InjectFamily(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        family_key = view_kwargs.get('family', None)
        if family_key:
            if not request.user.is_authenticated():
                raise Http404("Login required")
            family = get_object_or_404(models.Family, url_name=family_key)
            if request.user not in family.users.all():
                raise Http404("You are not part of this family")
            view_kwargs['family'] = family
