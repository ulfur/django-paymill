import sys
import django.dispatch

chargeback.executed         = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object with state set to chargeback
transaction.created         = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object
transaction.succeeded       = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object
transaction.failed          = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object

subscription.created        = django.dispatch.Signal( providing_args=('event',) ) #returns a subscription-object
subscription.updated        = django.dispatch.Signal( providing_args=('event',) ) #returns a subscription-object
subscription.deleted        = django.dispatch.Signal( providing_args=('event',) ) #returns a subscription-object
subscription.succeeded      = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object and a subscription-object
subscription.failed         = django.dispatch.Signal( providing_args=('event',) ) #returns a transaction-object and a subscription-object

refund.created              = django.dispatch.Signal( providing_args=('event',) ) #returns a refund-object
refund.succeeded            = django.dispatch.Signal( providing_args=('event',) ) #returns a refunds-object
refund.failed               = django.dispatch.Signal( providing_args=('event',) ) #returns a refunds-object

app.merchant.activated      = django.dispatch.Signal( providing_args=('event',) ) #returns a merchant-object if a connected merchant was activated
app.merchant.deactivated    = django.dispatch.Signal( providing_args=('event',) ) #returns a merchant-object if a connected merchant was deactivated
app.merchant.rejected       = django.dispatch.Signal( providing_args=('event',) ) #returns a merchant-object if a connected merchant was rejected
app.merchant.app.disabled   = django.dispatch.Signal( providing_args=('event',) ) #returns a merchant object if a connected merchant disabled your app

payout.transferred          = django.dispatch.Signal( providing_args=('event',) ) #returns an invoice-object with the payout sum for the invoice period
invoice.available           = django.dispatch.Signal( providing_args=('event',) ) #returns an invoice-object with the fees sum for the invoice period
client.updated              = django.dispatch.Signal( providing_args=('event',) ) #returns a client-object if a client was updated

def get_signal( name ):
    module = sys.modules[__name__]
    event_name = event.replace('.','_')
    return getattr( module, event_name, None )