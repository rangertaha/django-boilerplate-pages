# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import MenuView


urlpatterns = [
    url(r'^$', MenuView.as_view()),
]