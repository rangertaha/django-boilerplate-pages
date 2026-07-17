from django import template

# ``{% load menu %}`` requires this module-level Library instance.
register = template.Library()

"""
from apps.menu.models import Section, Category


register = template.Library()


@register.inclusion_tag('menu/snippets/menu.html')
def menu_sidebar(section=None):
    return {'section': section}


@register.inclusion_tag('menu/snippets/menu_item.html')
def menu_sidebar_item(page=None):
    return {'page': page}
"""
