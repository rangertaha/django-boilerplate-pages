# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import logging
import hashlib

#from django.contrib.auth.models import User
from django.conf import settings as django_settings
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

# Get an instance of a logger
logger = logging.getLogger(__name__)

STATUSES = (
    (0, _('Draft')),
    (1, _('Published')),
    (2, _('Hidden')),
)


class Page(MPTTModel):
    order = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=512, blank=True, null=True)
    slug = models.SlugField(max_length=512, blank=True, null=True, unique=True)
    subtitle = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    # Related
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    # Metadata
    created = models.DateTimeField(_('Created'), auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(_('Updated'), auto_now=False, auto_now_add=True)
    active = models.BooleanField(_('Active'), default=True)
    status = models.IntegerField(_('Status'), choices=STATUSES, default=0)


    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        ordering = ('order',)
        verbose_name_plural = "Pages"

    # It is required to rebuild tree after save, when using order for mptt-tree
    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        Page.objects.rebuild()

    def __unicode__(self):
        return self.slug


class Section(MPTTModel):
    order = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=64, blank=True, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    # Related
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    pages = models.ManyToManyField(Page, blank=True, limit_choices_to={'active': True})

    # Metadata
    created = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    public = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        ordering = ('order', )

    def __unicode__(self):
        return self.slug


@receiver(pre_save, sender=Section)
def slugify_section_name(sender, **kwargs):
    section = kwargs['instance']
    if section.slug is None or section.slug is '':
        section.slug = slugify(section.name)


@receiver(pre_save, sender=Page)
def slugify_page_title(sender, **kwargs):
    page = kwargs['instance']
    if page.slug is None or page.slug is '':
        page.slug = slugify(page.title)
