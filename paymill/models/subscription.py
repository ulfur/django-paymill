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

    offer  = models.ForeignKey( Offer, related_name='subscriptions' )
    client = models.ForeignKey( Client, related_name='subscriptions' )
    payment = models.ForeignKey( Payment, related_name='subscriptions' )

    def _create_paymill_object( self, client, offer, start_at=None ):
        payment = client.get_payment()
        return self.paymill.new_subscription( client.paymill_id, offer.paymill_id, payment.paymill_id, start_at=start_at )

    def _delete_paymill_object( self, *args, **kwargs ):
        self.cancel( )

    @classmethod
    def create( cls, client, offer ):
        i = super(Subscription, cls).create( client, offer )
        
        i.offer = offer
        i.client = client
        i.payment = client.get_payment( )
        
        return i

    def cancel( self ):
        self.paymill.cancelsubnow( self.paymill_id )
        self.canceled_at = datetime.now( )
        self.save( )