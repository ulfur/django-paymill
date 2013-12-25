#encoding: utf-8

import pymill

from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.generic import View

from .models import Transaction

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