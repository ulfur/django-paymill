#encoding: utf-8

import uuid

from django.core.urlresolvers import reverse
from django.conf import settings

from django.db import models
from .base import PaymillModel

from .choices import *

class Webhook( PaymillModel ):

    url = models.URLField( )
    secret = models.CharField( max_length=16 )
    livemode = models.BooleanField( default=False )
    event_type = models.CharField( max_length=100, choices=WEBHOOK_EVENTS )

    def get_url( self ):
        if not self.url:
            event = self.event_type.replace('.','_')
            path = reverse( 'paymill-webhook', args=(self.secret, event) )
            self.url = '%s%s'%(settings.PAYMILL_WEBHOOK_HOST, path)
        return self.url

    def _create_paymill_object( self ):
        if not self.secret:
            self.secret = uuid.uuid4().hex
        return self.paymill.new_webhook( self.get_url(), self.event_type )
        
    def save( self, *args, **kwargs ):
        if not self.paymill_id:
            ob = self._create_paymill_object( )
            self._update_from_paymill_object( ob )
        return super(Webhook, self).save(*args, **kwargs)
