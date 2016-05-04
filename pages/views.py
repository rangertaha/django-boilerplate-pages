#-*- coding:utf-8 -*-
"""
"""
# import the logging library
import logging

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required


from models import Section, Page
from forms import *
from signals import *
from models import *
from .mixins import NavBarMixin, PageMixin

# Get an instance of a logger
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'pages/index.html'


class SectionView(DetailView, NavBarMixin):
    model = Section
    template_name = 'pages/index.html'

    def get_queryset(self):
        return self.model.objects.filter(active=True, parent__isnull=True)


class PageView(DetailView, PageMixin):
    model = Page
    template_name = 'pages/index.html'

    def get_queryset(self):
        return self.model.objects.filter(active=True,
                                   slug=self.kwargs.get('slug', None))
