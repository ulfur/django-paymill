import sys
import django.dispatch

chargeback_executed         = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object with state set to chargeback
transaction_created         = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object
transaction_succeeded       = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object
transaction_failed          = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object

subscription_created        = django.dispatch.Signal( providing_args=('event',) ) #returns a subscription-object
subscription_updated        = django.dispatch.Signal( providing_args=('event',) ) #returns a subscription-object
subscription_deleted        = django.dispatch.Signal( providing_args=('event',) ) #returns a subscription-object
subscription_succeeded      = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object and a subscription-object
subscription_failed         = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object and a subscription-object

refund_created              = django.dispatch.Signal( providing_args=('event',) ) #returns a refund-object
refund_succeeded            = django.dispatch.Signal( providing_args=('event',) ) #returns a refunds-object
refund_failed               = django.dispatch.Signal( providing_args=('event',) ) #returns a refunds-object

app_merchant_activated      = django.dispatch.Signal( providing_args=('event',) ) #returns a merchant-object if a connected merchant was activated
app_merchant_deactivated    = django.dispatch.Signal( providing_args=('event',) ) #returns a merchant-object if a connected merchant was deactivated
app_merchant_rejected       = django.dispatch.Signal( providing_args=('event',) ) #returns a merchant-object if a connected merchant was rejected
app_merchant_app_disabled   = django.dispatch.Signal( providing_args=('event',) ) #returns a merchant object if a connected merchant disabled your app

payout_transferred          = django.dispatch.Signal( providing_args=('event',) ) #returns an invoice-object with the payout sum for the invoice period
invoice_available           = django.dispatch.Signal( providing_args=('event',) ) #returns an invoice-object with the fees sum for the invoice period
client_updated              = django.dispatch.Signal( providing_args=('event',) ) #returns a client-object if a client was updated

def get_signal( name ):
    module = sys.modules[__name__]
    event_name = name.replace( '.', '_' )
    return getattr( module, event_name, None )