#encoding: utf-8

from django.db import models

from .base import PaymillModel

from .offer import Offer
from .client import Client
from .payment import Payment

class Subscription( PaymillModel ):

    livemode = models.BooleanField( default=False )
    cancel_at_period_end = models.BooleanField( default=False )
    trial_start = models.DateTimeField( blank=True, null=True )
    trial_end = models.DateTimeField( blank=True, null=True )
    next_capture_at = models.DateTimeField( )
    canceled_at = models.DateTimeField( blank=True, null=True )
    start_at = models.DateTimeField( blank=True, null=True )
    
    offer  = models.ForeignKey( Offer, related_name='subscriptions' )
    client = models.ForeignKey( Client, related_name='subscriptions' )
    payment = models.ForeignKey( Payment, related_name='subscriptions' )
    
    def _create_paymill_object( self ):
        return self.paymill.new_subscription( self.client.id, self.offer.id, self.payment.id, start_at=self.start_at )

    def _delete_paymill_object( self, *args, **kwargs ):
        self.cancel( )
        
    def cancel( self ):
        self.paymill.cancelsubnow( self.id )
        self.canceled_at = datetime.now( )
        self.save( )
        
    def __unicode__( self ):
        return u'%s - %s (%s)'%( self.offer.name, self.client.email, self.id )