
import re, uuid
from urlparse import urlparse
from django.core.urlresolvers import reverse, resolve
from django.conf import settings

from pymill import Pymill

WEBHOOK_EVENTS = (
            u'chargeback.executed', 
            u'refund.created', 
            u'refund.succeeded', 
            u'refund.failed', 
            u'subscription.created', 
            u'subscription.updated', 
            u'subscription.deleted', 
            u'subscription.succeeded', 
            u'subscription.failed', 
            u'transaction.created', 
            u'transaction.succeeded', 
            u'transaction.failed', 
            u'app.merchant.activated', 
            u'invoice.available', 
            u'payout.transferred', 
            u'app.merchant.deactivated', 
            u'app.merchant.rejected', 
            u'client.updated', 
            u'app.merchant.app.disabled'
        )

def get_webhook( ):
    paymill = Pymill( settings.PAYMILL_PRIVATE_KEY )
    webhooks = paymill.get_webhooks( )
    for hook in webhooks:
        url = urlparse( hook.url )
        try:
            match = resolve( url.path )
            if match.url_name == 'paymill-webhook':
                return match.kwargs.get('secret',None)
        except:
            pass
    return None

def validate_webhook( secret ):
    return secret == get_webhook( )

def install_webhook( ):
    paymill = Pymill( settings.PAYMILL_PRIVATE_KEY )
    secret = uuid.uuid4().hex
    url = 'http://%s%s'%( settings.PAYMILL_WEBHOOK_HOST, reverse( 'paymill-webhook', args=[secret,] ) )
    paymill.new_webhook( url, WEBHOOK_EVENTS )
    return secret

def init_webhook( ):
    print 'Looking for webhook'
    secret = get_webhook( )
    if not secret:
        print 'Webhook not found, installing'
        secret = install_webhook( )
    print 'Webhook ready: %s'%secret
    
    return secret

    