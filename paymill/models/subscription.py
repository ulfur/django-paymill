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

    offer  = models.ForeignKey( Offer )
    client = models.ForeignKey( Client )
    payment = models.ForeignKey( Payment )

    def __create_paymill_object( self, client, offer ):
        payment = client.get_payment()
        return self.paymill.newsub( client.paymill_id, offer.paymill_id, payment.paymill_id )
        
    @classmethod
    def create( cls, client, offer ):
        o = super(Subscription, cls).create(client, offer)
        
        o.offer = offer
        o.client = client
        o.payment = client.get_payment( )
        o.save( )
        
        return o

    def cancel( self ):
        self.paymill.cancelsubnow( self.external_ref )
        self.canceled_at = datetime.now()
        self.save()

    def delete( self, *args, **kwargs ):
        self.cancel( )
        return super(Subscription, self).delete(*args, **kwargs)
