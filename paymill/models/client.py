#encoding: utf-8

from django.db import models
from .base import PaymillModel

class Client( PaymillModel ):

    description = models.TextField( null=True, blank=True )
    email = models.EmailField( null=True, blank=True  )

    def __create_paymill_object( self, email, description ):
        return self.paymill.newclient( email, description )

    def add_payment( self, token ):
        p = Payment.create( token, client=self )

    def delete( self, delete_cards=True, *args, **kwargs ):
        for payment in self.payments.all():
            payment.delete()
        self.paymill.delclient( self.external_ref )
        return super(Client, self).delete(*args, **kwargs)

    def get_payment( self ):
        pms = self.payments.all()
        if len(pms)>0:
            return pms[0]
        return None

    @property
    def has_payment( self ):
        return self.get_payment() is not None

    def __unicode__( self ):
        return u'%s - "%s"'%(self.email, self.description)
