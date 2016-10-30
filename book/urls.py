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
    url(r'^home$', views.standard_page, name="home"),
    url(r'^photo/(?P<photo>[0-9]+)$', views.photo_view, name="photo"),
    url(r'^new_post$', views.new_post, name="new_post"),
    url(r'^member/(?P<member>[0-9]+)$', views.member_view, name="member")
]


urlpatterns = [
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^family_list', views.standard_page, name="families"),
    url(r'^images/(?P<path>[A-Za-z0-9\-\.]+)', views.get_image),
    #url(r'^batch_create', views.batch_create)
    url('^(?P<family>[A-Za-z0-9\-]+)/', include(family_patterns, namespace="family")),
]
