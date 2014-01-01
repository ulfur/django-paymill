#encoding: utf-8

import json
import pymill

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .signal import get_signal
from .models import *

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
        event = json.loads( request.body )

        #Process Paymill objects
        f = getattr( self, event['event_type'].replace('.','_'), None )
        if f:
            f( event )
            
        signal = get_signal( event['event_type'] )
        signal.send( sender=self, event=event )
        
        return HttpResponse( )

    def client_updated( self, event ):
        Client.update_or_create( event['event_resource'] )
'''
    {
        "event":{
            "event_type":"client.updated",
            "event_resource":{
                "id":"client_cdcc9709ffcef07f9286",
                "email":"ulfurk@ulfurk.com",
                "description":"Ulfur Kristjansson (Are we cooking with gas?)",
                "created_at":1388418081,
                "updated_at":1388831265,
                "app_id":null,
                "payment":[],
                "subscription":null
            },
            "created_at":1388831265,
            "app_id":null
        }
    }
'''
