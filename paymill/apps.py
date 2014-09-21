from django.apps import AppConfig

from .webhooks import init_webhook

class PaymillConfig( AppConfig ):
    name = 'paymill'
    verbose_name = 'Paymill'
    
    def ready( self ):
        init_webhook( )