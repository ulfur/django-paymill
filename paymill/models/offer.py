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

    def __create_paymill_object( self, name, amount, interval='1 MONTH', currency='EUR' ):
        return self.paymill.newoffer( name=name, amount=amount, interval=interval, currency=currency )
            
    def save( self, *args, **kwargs ):
        if self.external_ref:
            res = self.create_paymill_object( self.name, self.amount, interval=self.interval, currency=self.currency )
        else:
            res = self.paymill.newoffer( amount=self.amount, interval=self.interval, currency=self.currency, name=self.name )
        self.update_from_paymilldata( res['data'] )
        return super(Offer, self).save(*args, **kwargs)
        
    def subscribe( self, client ):
        return Subscription.create( client, self )