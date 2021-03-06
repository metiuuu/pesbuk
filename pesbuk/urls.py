"""pesbuk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from activity import views as activiy_views

urlpatterns = [
    url(r'^create_user', csrf_exempt(activiy_views.create_user), name='create_user'),
    url(r'^create_activity', csrf_exempt(activiy_views.create_activity), name='create_activity'),
    url(r'^get_feed', csrf_exempt(activiy_views.get_feed), name='get_feed'),
    url(r'^create_friendship', csrf_exempt(activiy_views.create_friendship), name='friendship'),
]
