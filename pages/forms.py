#-*- coding:utf-8 -*-
"""
"""
# import the logging library
import logging

from django.forms import ModelForm
from django.conf import settings


from models import *

# Get an instance of a logger
logger = logging.getLogger(__name__)

"""
class ToolForm(ModelForm):
    class Meta:
        model = Tool
        widgets = {
            'name': RedactorWidget(editor_options={'lang': 'en'}),
            'tutorial': AutosizedTextarea(attrs={'class': 'col-md-12'}),
        }

        from django_markdown.fields import MarkdownFormField
from django_markdown.widgets import MarkdownWidget
class MyCustomForm(forms.Form):
    content = forms.CharField(widget=MarkdownWidget())
    content2 = MarkdownFormField()

"""

