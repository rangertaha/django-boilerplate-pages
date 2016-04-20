# -*- coding:utf-8 -*-
"""
"""
from __future__ import unicode_literals

from django.conf.urls import url

from views import SectionView, PageView, IndexView


urlpatterns = [
    url(r'^$',  IndexView.as_view(), name='index'),

    url(r'^(?P<slug>[\w-]+)$',  SectionView.as_view(), name='section'),

    url(r'^(?P<section>[\w-]+)/(?P<slug>[\w-]+)$',
        PageView.as_view(), name='top-page'),

    url(r'^(?P<section>[\w-]+)/(?P<parents>.*)/(?P<slug>[\w-]+)$',
        PageView.as_view(), name='child-page'),
]
