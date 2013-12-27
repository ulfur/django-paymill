#encoding: utf-8

from django.db import models
from .base import PaymillModel

from .client import Client

class Payment( PaymillModel ):

    client = models.ForeignKey( Client, related_name='payments' )
    type = models.CharField( max_length=20 )
    card_type = models.CharField( max_length=10 )
    country = models.CharField( max_length=100, blank=True, null=True )
    expire_month = models.PositiveIntegerField()
    expire_year = models.PositiveIntegerField()
    card_holder = models.CharField( max_length=30, blank=True, null=True )
    last4 = models.CharField( max_length=4 )

    def __create_paymill_object( self, token, client=None ):
        return self.paymill.newcard( token, client = client.paymill_id if client else None  )
    
    @classmethod
    def create( cls, *args, **kwargs ):
        o = super(Payment, cls).create(*args, **kwargs)
        o.client = kwargs.get( 'client', None )
        return o
        
    def delete( self, *args, **kwargs ):
        self.paymill.delcard( self.external_ref )
        return super(Payment, self).delete(*args, **kwargs)

    def __unicode__( self ):
        return u'%s - %s (**** ***** **** %s)'%(self.card_holder,self.card_type, self.last4)
