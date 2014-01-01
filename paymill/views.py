#encoding: utf-8

import pymill

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from . import signals

from .models import Transaction, Webhook

class PaymillTransactionView( View ):

    def post( self, request, *args, **kwargs ):

        amount = request.POST.get( 'payment_amount', 0 )
        currency = request.POST.get( 'payment_currency', 'USD' )
        description = request.POST.get( 'payment_description', '' )
        next = request.POST.get( 'next', getattr( settings, 'PAYMILL_SUCCESS', '/' ) )

        p = pymill.Pymill( settings.PAYMILL_PRIVATE_KEY )
        card = p.newcard( request.POST.get('paymillToken') )["data"]
        transaction = p.transact( amount=amount, currency=currency, description=description, payment=card["id"])["data"] 

        if getattr( settings, 'PAYMILL_SAVE_TRANSACTIONS', True ):
            transaction = Transaction.parse_transaction( transaction )

        return HttpResponseRedirect( next  )

class PaymillAddCardView( View ):

    def post( self, request, *args, **kwargs ):

        next = request.POST.get( 'next', getattr( settings, 'PAYMILL_SUCCESS', '/' ) )
        client = request.session.get( 'paymill_client', None )
        client.add_payment( request.POST.get('paymillToken') )

        return HttpResponseRedirect( next  )

class WebhookView( View ):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WebhookView, self).dispatch(*args, **kwargs)
        
    def post( self, request, *args, **kwargs ):
        print request.body
#       Process Paymill objects

#       signal = getattr( signals, event_name )
#       signal.send( sender=self, event=event )
        
        return HttpResponse( )

