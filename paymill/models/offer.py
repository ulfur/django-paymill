#encoding: utf-8

from django.db import models
from django.utils.text import slugify

from .base import PaymillModel

from .choices import *

class Offer( PaymillModel ):

    name = models.CharField( max_length='50' )
    amount = models.PositiveIntegerField( )
    currency = models.CharField( max_length=3, choices=CURRENCY_CHOICES )
    interval = models.CharField( max_length=20, choices=INTERVAL_CHOICES )
    trial_period_days = models.PositiveIntegerField( blank=True )

    slug = models.SlugField( blank=True, null=True )
    
    def _create_paymill_object( self ):
        return self.paymill.new_offer( self.amount, name=self.name, interval=self.interval, currency=self.currency )

    def _delete_paymill_object( self ):
        for subscription in self.subscriptions.all( ):
            subscription.cancel( )
        self.paymill.delete_offer( self.id )
            
    def subscribe( self, client, start_at=None ):
        s = self.subscriptions.create( client=client, payment=client.get_payment(), offer=self )
        s.save( )
        return s
        
    def save( self, *args, **kwargs ):
        if not self.slug:
            i = 2
            self.slug = slugify( self.name )
            while Offer.objects.filter( slug=self.slug ).count()>0:
                self.slug = slugify( '%s %i'%(self.name,i) )
                i += 1
        return super(Offer, self).save(*args, **kwargs)

    def __unicode__( self ):
        return u'%s (%s)'%( self.name, self.id )