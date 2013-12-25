#encoding: utf-8

from datetime import datetime
import pymill
from django.contrib import admin
from django.conf import settings

from .models import *

class TransactionAdmin( admin.ModelAdmin ):
    date_hierarchy = 'created_at'
    list_filter = ( 'status', 'refunded' )
    list_display = ( 'payment', 'status', 'origin_amount', 'currency', 'refunded' )
    exclude = ( 'livemode', 'amount', 'client' )
    actions = ['refund']
    fields = ( 
                        ('status', 'response_code'),
                        ('created_at', 'updated_at'),
                        ('origin_amount', 'currency'),
                        'payment',
                        'external_ref',
                        'description',
                        ('refunded','refunded_at') 
                    )

    readonly_fields = ( 
                        'status', 
                        'response_code', 
                        'created_at',
                        'updated_at',
                        'origin_amount',
                        'currency',
                        'payment',
                        'external_ref',
                        'description', 
                        'refunded',
                        'refunded_at'
                    )

    def refund( self, request, queryset ):
        p = pymill.Pymill( settings.PAYMILL_PRIVATE_KEY )
        refunded = 0
        for transaction in queryset:
            refund = p.refund( transaction.external_ref, transaction.origin_amount )['data']
            if refund['response_code'] == 20000:
                transaction.refunded = True
                transaction.refunded_at = datetime.utcfromtimestamp( refund['created_at'] )
                transaction.save()
                refunded += 1
        message = "1 transaction was" if refunded == 1 else "%s transactions were" % refunded
        self.message_user(request, "%s successfully refunded" % message)	
    refund.short_description = 'Refund transaction'

admin.site.register( Transaction, TransactionAdmin )

admin.site.register( Client )
admin.site.register( Payment )
admin.site.register( WebHook )
