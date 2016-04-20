#-*- coding:utf-8 -*-
"""
"""
import logging
import random

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.base import ContextMixin
from django.views.generic import View
from django.conf import settings

from .models import Section


logger = logging.getLogger(__name__)


class NavBarMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(NavBarMixin, self).get_context_data(**kwargs)
        context['sections'] = Section.objects.filter().distinct()
        return context


class MenuMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        section = self.kwargs.get('section', None)
        context['section'] = Section.objects.get(slug=section)
        return context


class PageMixin(NavBarMixin, MenuMixin):
    pass








"""
class ContactModalMixin(SuccessMessageMixin, FormView):
    form_class = ContactForm
    success_url = '/'
    success_message = "Successfully sent message..."

    def form_valid(self, form):
        form.send_email()
        return super(ContactModalMixin, self).form_valid(form)


class MetaMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(MetaMixin, self).get_context_data(**kwargs)
        context['title'] = random.choice(settings.TITLE)
        context['description'] = random.choice(settings.DESCRIPTION)
        context['keywords'] = random.choice(settings.KEYWORDS)
        context['author'] = settings.AUTHOR
        return context


class FooterMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(FooterMixin, self).get_context_data(**kwargs)
        context['footer_text'] = settings.FOOTER_TEXT
        context['top_authors'] = Author.objects.filter()[:10]
        context['top_licenses'] = License.objects.filter()[:10]
        context['top_tools'] = Tool.objects.filter()[:10]
        context['top_categories'] = Category.objects.filter()[:10]
        context['top_sections'] = Section.objects.filter()[:10]
        context['top_links'] = Link.objects.filter()[:10]
        context['top_languages'] = ProgrammingLanguage.objects.filter()[:10]
        return context


class NavBarMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(NavBarMixin, self).get_context_data(**kwargs)
        context['sections'] = Section.objects.filter(active=True, parent__isnull=True).distinct()
        context['name'] = settings.BRAND_NAME
        return context


class SiteMixin(FooterMixin, NavBarMixin):
    def get_context_data(self, **kwargs):
        context = super(SiteMixin, self).get_context_data(**kwargs)
        section = self.kwargs.get('section', None)
        category = self.kwargs.get('category', None)
        tool = self.kwargs.get('tool', None)

        if section:
            context['section'] = Section.objects.get(slug=section)
        if category:
            context['category'] = Category.objects.get(slug=category)
        if tool:
            context['tool'] = tool

        return context
"""

