"""InterestFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from IF_App import views

urlpatterns = [
    url(r'^$', views.main, name='index'),
    url(r'^canton/(?P<canton_name>.+)/$', views.canton, name='canton'),
    url(r'^economic_sectors/$', views.economic_sectors),
    url(r'^candidate/(?P<candidate_id>.+)/$', views.candidate_profile, name='candidate_profile'),
    url(r'^cantons_list/$', views.cantons_list, name='cantons_list'),
    url(r'^data_viz/$', views.data_viz, name='data_viz'),
    url(r'^admin/', include(admin.site.urls)),
]
