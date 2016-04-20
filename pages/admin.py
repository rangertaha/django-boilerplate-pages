# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
import logging

from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from models import Section, Page


# Get an instance of a logger
logger = logging.getLogger(__name__)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'active', 'name', 'description')
    search_fields = ('name', 'order', 'description', 'text')
    list_editable = ('active', )
    list_display_links = ('id', 'name', 'description')
    raw_id_fields = ('pages',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'title', 'status')
    search_fields = ('id', 'active', 'title', 'subtitle', 'description', 'body')
    ordering = ['order']
    list_display_links = ('id',)
    list_editable = ('order', 'title', 'status')
    list_filter = ('created', 'parent', 'section__name')
    raw_id_fields = ('parent', )

