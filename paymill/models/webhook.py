#encoding: utf-8

from django.db import models
from .base import PaymillModel

from .choices import *

class WebHook( PaymillModel ):

    url = models.URLField( )
    livemode = models.BooleanField( default=False )
    event_type = models.CharField( max_length=100, choices=WEBHOOK_EVENTS )
