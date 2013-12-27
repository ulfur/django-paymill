#encoding: utf-8

from datetime import datetime
from django.db import models
from django.conf import settings

from pymill import Pymill

class PaymillModel( models.Model ):

    paymill = Pymill( settings.PAYMILL_PRIVATE_KEY )
    
    external_ref = models.CharField( max_length=100 )
    created_at = models.DateTimeField( )
    updated_at = models.DateTimeField( )

    class Meta:
        abstract = True

    @property
    def paymill_id( self ):
        return self.external_ref

    def __update_from_paymilldata( self, data ):
        print data
        for k, v in data.items():
            k = 'external_ref' if k == 'id' else k
            if hasattr( self, k ) and v is not None:
                ftype = type( self._meta.get_field( k ) )
                if ftype == models.DateTimeField:
                    v = datetime.utcfromtimestamp( v )
                print k, v
                setattr( self, k, v )
        return self

    def __create_paymill_object( self, *args, **kwargs ):
        raise NotImplementedError
                
    @classmethod
    def create( cls, *args, **kwargs ):
        o = cls()

        res = o.__create_paymill_object( *args, **kwargs )
        o.__update_from_paymilldata( res['data'] )
        o.save( )

        return o