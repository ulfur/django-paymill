#encoding: utf-8

from datetime import datetime
from django.db import models
from django.conf import settings

from pymill import Pymill, PaymillObject

def paymill_dict( ob ):
    if isinstance( ob, PaymillObject ):
        return ob.__dict__
    elif isinstance( ob, dict ):
        return ob
    raise TypeError( 'paymill_dict expects either PaymillObject or dict' )

class PaymillModel( models.Model ):

    paymill = Pymill( settings.PAYMILL_PRIVATE_KEY )
    
    external_ref = models.CharField( max_length=100, db_index=True )
    created_at = models.DateTimeField( )
    updated_at = models.DateTimeField( )
    
    class Meta:
        app_label = 'paymill'
        abstract = True
        
    @property
    def paymill_id( self ):
        return self.external_ref

    def _update_from_paymill_object( self, ob ):
        ob = paymill_dict( ob )
        updated = False
        for k, v in ob.items():
            k = 'external_ref' if k == 'id' else k
            if hasattr( self, k ) and v is not None:
                ftype = type( self._meta.get_field( k ) )
                if ftype == models.DateTimeField:
                    v = datetime.utcfromtimestamp( v )
                updated = updated or getattr(self,k) != v
                setattr( self, k, v )
        return updated

    def _create_paymill_object( self, *args, **kwargs ):
        raise NotImplementedError( '_create_paymill_object not implemented for this class' )

    def _delete_paymill_object( self ):
        raise NotImplementedError( '_delete_paymill_object not implemented for this class' )
        
    def delete( self, *args, **kwargs ):
        self._delete_paymill_object( )
        return super(PaymillModel, self).delete(*args, **kwargs)
    
    @classmethod
    def update_or_create( cls, ob ):
        ob = paymill_dict( ob )
        try:
            o = cls.objects.get( external_ref=ob['id'] )
        except:
            o = cls( )
        o._update_from_paymill_object( ob )
        return o

    @classmethod
    def create( cls, *args, **kwargs ):
        i = cls( )
        ob = i._create_paymill_object( *args, **kwargs )
        i._update_from_paymill_object( ob )
        
        return i
