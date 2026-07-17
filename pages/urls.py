""" """

from django.urls import re_path

from .views import SectionView, PageView, IndexView


urlpatterns = [
    re_path(r"^$", IndexView.as_view(), name="index"),
    re_path(r"^(?P<slug>[\w-]+)$", SectionView.as_view(), name="section"),
    re_path(
        r"^(?P<section>[\w-]+)/(?P<slug>[\w-]+)$", PageView.as_view(), name="top-page"
    ),
    re_path(
        r"^(?P<section>[\w-]+)/(?P<parents>.*)/(?P<slug>[\w-]+)$",
        PageView.as_view(),
        name="child-page",
    ),
]
