#-*- coding:utf-8 -*-
"""
"""
# Import the logging library
import logging

# Import signals
from django.core.signals import request_started, request_finished


# Get an instance of a logger
logger = logging.getLogger(__name__)


