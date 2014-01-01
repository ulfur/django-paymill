#encoding: utf-8

from django.db import models
from .base import PaymillModel

from .choices import *

class Offer( PaymillModel ):

    name = models.CharField( max_length='50' )
    amount = models.PositiveIntegerField( )
    currency = models.CharField( max_length=3, choices=CURRENCY_CHOICES )
    interval = models.CharField( max_length=20, choices=INTERVAL_CHOICES )
    trial_period_days = models.PositiveIntegerField( blank=True )

    def _create_paymill_object( self, name, amount, interval='1 MONTH', currency='EUR' ):
        return self.paymill.new_offer( amount, name=name, interval=interval, currency=currency )

    def _delete_paymill_object( self ):
        for subscription in self.subscriptions.all( ):
            subscription.cancel( )
        self.paymill.delete_offer( self.paymill_id )
            
    def save( self, *args, **kwargs ):
        if not self.paymill_id:
            ob = self._create_paymill_object( self.name, self.amount, interval=self.interval, currency=self.currency )
            self._update_from_paymill_object( ob )
        return super(Offer, self).save(*args, **kwargs)
        
    def subscribe( self, client ):
        s = self.subscriptions.create_object( client, self )
        s.save( )
        return s