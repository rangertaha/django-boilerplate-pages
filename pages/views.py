""" """

# import the logging library
import logging

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView


from .models import Section, Page
from .forms import *
from .signals import *
from .mixins import NavBarMixin, PageMixin

# Get an instance of a logger
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "pages/index.html"


class SectionView(DetailView, NavBarMixin):
    model = Section
    template_name = "pages/index.html"

    def get_queryset(self):
        return self.model.objects.filter(active=True, parent__isnull=True)


class PageView(DetailView, PageMixin):
    model = Page
    template_name = "pages/index.html"

    def get_queryset(self):
        return self.model.objects.filter(
            active=True, slug=self.kwargs.get("slug", None)
        )
