#encoding: utf-8

from django.db import models
from .base import PaymillModel

from .client import Client
from .payment import Payment

from .choices import *

class Transaction( PaymillModel ):
    
    status = models.CharField( max_length=16 )
    response_code = models.PositiveIntegerField( )
    description = models.TextField( null=True, blank=True )

    #refunds
    #invoices
    
    livemode = models.BooleanField( default=False )
    origin_amount = models.PositiveIntegerField( )

    #preauthorization

    payment = models.ForeignKey( Payment, related_name='transactions' )
    currency = models.CharField( max_length=3, choices=CURRENCY_CHOICES )
    amount = models.CharField( max_length=10 )
    client = models.ForeignKey( Client, related_name='transactions' )

    refunded = models.BooleanField( default=False )
    refunded_at = models.DateTimeField( null=True, blank=True )

    def __unicode__( self ):
        return u'%s - %s'%(self.payment, self.status)

    @classmethod
    def parse_transaction( t ):

        client = Client.update_or_create( t['client'] )
        payment = Payment.update_or_create( t['payment'] )
        transaction = Transaction.update_or_create( t )
        
        return transaction