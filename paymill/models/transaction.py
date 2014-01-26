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
    
    livemode = models.BooleanField( )
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

        client, created = Client.objects.get_or_create( id=t['client']['id'], defaults = {
            'description' : t['client']['description'],
            'created_at'  : datetime.utcfromtimestamp( t['client']['created_at'] ),
            'updated_at'  : datetime.utcfromtimestamp( t['client']['updated_at'] ),
            'email' : t['client']['email'],
            #'payment':,
            #'subscription':
        })

        if not created: #Assuming we might have updated information
            client.description = t['client']['description']
            client.created_at = datetime.utcfromtimestamp( t['client']['created_at'] )
            client.updated_at = datetime.utcfromtimestamp( t['client']['updated_at'] )
            client.email = t['client']['email']
            #client.payment = 
            #client.subscription =
            client.save( )

        payment, created = Payment.objects.get_or_create( id=t['payment']['id'], defaults = {
            'expire_month'  : t['payment']['expire_month'],
            'expire_year'   : t['payment']['expire_year'],
            #'country'      :,
            'created_at'    : datetime.utcfromtimestamp( t['payment']['created_at'] ),
            'updated_at'    : datetime.utcfromtimestamp( t['payment']['updated_at'] ),
            'card_holder'   : t['payment']['card_holder'],
            'card_type'     : t['payment']['card_type'],
            'last4'         : t['payment']['last4'],
            'client'        : client,
            'type'          : t['payment']['type'],
        })

        transaction = Transaction( )
        transaction.status = t['status']
        transaction.response_code = t['response_code']
        transaction.description = t['description']
        #transaction.refunds = 
        #transaction.invoices =
        transaction.created_at = datetime.utcfromtimestamp( t['created_at'] )
        transaction.updated_at = datetime.utcfromtimestamp( t['updated_at'] )
        transaction.livemode = t['livemode']
        transaction.origin_amount = t['origin_amount']
        #transaction.preauthorization =
        transaction.currency = t['currency']
        transaction.amount = t['amount']
        transaction.payment = payment
        transaction.client = client	
        transaction.id = t['id']
        transaction.save( )

        return transaction