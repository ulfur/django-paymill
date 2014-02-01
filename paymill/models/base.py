#encoding: utf-8

from datetime import datetime
from django.db import models
from django.conf import settings

import pytz
utc=pytz.UTC

from pymill import Pymill, PaymillObject

def paymill_dict( ob ):
    if isinstance( ob, PaymillObject ):
        return ob.__dict__
    elif isinstance( ob, dict ):
        return ob
    raise TypeError( 'paymill_dict expects either PaymillObject or dict' )
        
class PaymillModel( models.Model ):

    paymill = Pymill( settings.PAYMILL_PRIVATE_KEY )
    
    id = models.CharField( max_length=80, db_index=True, primary_key=True )
    created_at = models.DateTimeField( )
    updated_at = models.DateTimeField( )
    
    class Meta:
        app_label = 'paymill'
        abstract = True
        
    def _update_from_paymill_object( self, ob ):
        ob = paymill_dict( ob )                                 # Make sure we have a dict rather than a PaymillObject (from Pymill)
        updated = False                                         # Nothing has been updated yet
        for k, v in ob.items( ):                                # Iterate over all the items of the object dict
            if v is not None and (hasattr( self, k ) or hasattr( self, '%s_id'%k )):            # If this model has this field and the value is not None
                ftype = self._meta.get_field( k )               # Let's type check the field
                if isinstance( ftype, models.DateTimeField):    # If the field is a DateTimeField ...
                    v = datetime.utcfromtimestamp( float(v) )   # we know the value must be a datetime object
                    v = utc.localize( v )
                if isinstance( ftype, models.ForeignKey ):      # If the field is a ForeignKey ...
                    k = '%s_id'%k                               # we know the value is an object-id and we must use the corresponding field name
                    if isinstance(v,dict):                      # What we have might not be the actual id of the object
                        v = v['id']                             # but a dict containing all its' attributes
                        
                if getattr(self,k) != v:                        # If the current value and the new value differ ...
                    setattr( self, k, v )                       # set the current value to the new value
                updated = updated or getattr(self,k) != v       # Have we updated anything yet?
        return updated                                          # Let the caller know if anything got updated

    def _create_paymill_object( self, *args, **kwargs ):
        raise NotImplementedError( '_create_paymill_object not implemented for this class' )

    def save( self, *args, **kwargs ):
        if not self.id:
            ob = self._create_paymill_object( )
            if ob:
                self.id = ob.id
                self._update_from_paymill_object( ob )
        return super(PaymillModel, self).save(*args, **kwargs)

    def _delete_paymill_object( self ):
        raise NotImplementedError( '_delete_paymill_object not implemented for this class' )
        
    def delete( self, *args, **kwargs ):
        self._delete_paymill_object( )
        return super(PaymillModel, self).delete(*args, **kwargs)
            
    @classmethod
    def update_or_create( cls, ob ):
        ob = paymill_dict( ob )
        created = False
        try:
            djob = cls.objects.get( id=ob['id'] )
        except:
            djob = cls( )
            created = True
            
        djob._update_from_paymill_object( ob )
        djob.save( )
        return djob
