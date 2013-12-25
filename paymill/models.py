#encoding: utf-8

from datetime import datetime
from django.db import models
from django.conf import settings

from pymill import Pymill
pymill = Pymill( settings.PAYMILL_PRIVATE_KEY )

from .event_choices import WEBHOOK_EVENTS

class PaymillModel( models.Model ):

    external_ref = models.CharField( max_length=100 )
    created_at = models.DateTimeField( )
    updated_at = models.DateTimeField( )

    def update_from_paymilldata( self, data ):
        for k, v in data.items():
            k = 'external_ref' if k == 'id' else k
            if hasattr( self, k ):
                ftype = type( self._meta.get_field( k ) )
                if ftype == models.DateTimeField:
                    v = datetime.utcfromtimestamp( v )
                setattr( self, k, v )
        return self

    @property
    def paymill_id( self ):
        return self.external_ref

    @classmethod
    def create_from_paymilldata( cls, data ):
        c = cls()
        return c.update_from_paymilldata( data )

class Client( PaymillModel ):

    description = models.TextField( null=True, blank=True )
    email = models.EmailField( null=True, blank=True  )

    @classmethod
    def create( cls, email, description ):
        res = pymill.newclient( email, description )
        c = cls.create_from_paymilldata( res['data'] )
        c.save()
        return c

    def add_payment( self, token ):
        p = Payment.create( token, client=self )

    def delete( self, delete_cards=True, *args, **kwargs ):
        for payment in self.payments.all():
            payment.delete()
        pymill.delclient( self.external_ref )
        return super(Client, self).delete(*args, **kwargs)

    def __unicode__( self ):
        return u'%s - "%s"'%(self.email, self.description)

    def get_payment( self ):
        pms = self.payments.all()
        if len(pms)>0:
            return pms[0]
        return None

    @property
    def has_payment( self ):
        return self.get_payment() is not None

class Payment( PaymillModel ):

    client = models.ForeignKey( Client, related_name='payments' )
    type = models.CharField( max_length=20 )
    card_type = models.CharField( max_length=10 )
    country = models.CharField( max_length=100, blank=True, null=True )
    expire_month = models.PositiveIntegerField()
    expire_year = models.PositiveIntegerField()
    card_holder = models.CharField( max_length=30, blank=True, null=True )
    last4 = models.CharField( max_length=4 )

    @classmethod
    def create( cls, token, client=None ):
        cref = client.external_ref if client else None
        res = pymill.newcard( token, client=cref )
        p = cls.create_from_paymilldata( res['data'] )
        p.client = client
        p.save( )
        return p

    def delete( self, *args, **kwargs ):
        pymill.delcard( self.external_ref )
        return super(Payment, self).delete(*args, **kwargs)

    def __unicode__( self ):
        return u'%s - %s (**** ***** **** %s)'%(self.card_holder,self.card_type, self.last4)

class Subscription( PaymillModel ):

    livemode = models.BooleanField( default=False )
    cancel_at_period_end = models.BooleanField( default=False )
    trial_start = models.DateTimeField( blank=True, null=True )
    trial_end = models.DateTimeField( blank=True, null=True )
    next_capture_at = models.DateTimeField( )
    canceled_at = models.DateTimeField( blank=True, null=True )

    payment = models.ForeignKey( Payment )
    client = models.ForeignKey( Client )

    @classmethod
    def create( cls, client, offer_id ):
        cref = client.external_ref if client else None
        res = pymill.newsub( cref, offer_id, client.get_payment().external_ref )
        s = cls.create_from_paymilldata( res['data'] )
        s.client = client
        s.payment = client.get_payment()
        s.save( )
        return s

    def cancel( self ):
        pymill.cancelsubnow( self.external_ref )
        self.canceled_at = datetime.now()
        self.save()

    def delete( self, *args, **kwargs ):
        self.cancel( )
        return super(Subscription, self).delete(*args, **kwargs)

class WebHook( PaymillModel ):
    
    url = models.URLField( )
    livemode = models.BooleanField( default=False )
    event_type = models.CharField( max_length=100, choices=WEBHOOK_EVENTS )

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
    currency = models.CharField( max_length=3 )
    amount = models.CharField( max_length=10 )
    client = models.ForeignKey( Client, related_name='transactions' )

    refunded = models.BooleanField( default=False )
    refunded_at = models.DateTimeField( null=True, blank=True )

    def __unicode__( self ):
        return u'%s - %s'%(self.payment, self.status)

    @classmethod
    def parse_transaction( t ):

        client, created = Client.objects.get_or_create( external_ref=t['client']['id'], defaults = {
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

        payment, created = Payment.objects.get_or_create( external_ref=t['payment']['id'], defaults = {
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
        transaction.external_ref = t['id']
        transaction.save( )

        return transaction