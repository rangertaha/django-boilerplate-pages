""" """

import logging

from django.contrib import admin
from .models import Section, Page


# Get an instance of a logger
logger = logging.getLogger(__name__)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "active", "name", "description")
    search_fields = ("name", "slug", "description", "text")
    list_editable = ("active",)
    list_display_links = ("id", "name", "description")
    raw_id_fields = ("pages",)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "title", "status")
    search_fields = ("title", "slug", "subtitle", "description", "body")
    ordering = ["order"]
    list_display_links = ("id",)
    list_editable = ("order", "title", "status")
    list_filter = ("created", "parent", "section__name")
    raw_id_fields = ("parent",)
