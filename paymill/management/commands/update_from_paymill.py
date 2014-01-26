from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from paymill.models import *
import pymill


class Command(BaseCommand):
#    args = '<poll_id poll_id ...>'
    help = 'Update django structures with current paymill data'

    def update_from_class( self, klass ):
        plural_class_name = '%ss'%klass.__name__.lower()
        print 'Updating %s...'%plural_class_name,
        paymill = pymill.Pymill( settings.PAYMILL_PRIVATE_KEY )
        f = getattr( paymill, 'get_%s'%plural_class_name, None )

        if f:
            try:
                objects = f( )
                for o in objects:
                    i = klass.update_or_create( o )
                print ' DONE'
                return
            except Exception as e:
                raise e
        print ' FAILED'
        
    def handle(self, *args, **options):
        self.update_from_class( Client )
        self.update_from_class( Offer )
        self.update_from_class( Subscription )