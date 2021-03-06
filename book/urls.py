"""FamilyBook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from book import views


family_patterns = [
    url(r'^$', views.home),
    url(r'^home$', views.home, name="home"),
    url(r'^new_post$', views.new_post, name="new_post"),
    url(r'^new_event', views.standard_page, name="new_event"),
    url(r'^invite$', views.invite, name="invite"),
    url(r'^profile$', views.member_edit, name="member_edit"),

]


urlpatterns = [
    url(r'^$', views.login),
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^family_list', views.standard_page, name="families"),
    url(r'^images/(?P<path>[A-Za-z0-9\-\.]+)', views.get_image),
    url(r'^batch_create', views.batch_create),
    url(r'^accept/(?P<key>[A-Za-z0-9]+)$', views.accept, name="accept"),
    url(r'^account$', views.account, name="account"),
    url('^(?P<family>[A-Za-z0-9\-]+)/', include(family_patterns, namespace="family")),
]
