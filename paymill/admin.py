#encoding: utf-8

from datetime import datetime
import pymill
from django.contrib import admin
from django.conf import settings

from .models import *

class ClientAdmin( admin.ModelAdmin ):
    list_display = ('email', 'description', 'id', 'created_at')
    search_fields = ( 'email', )
    fieldsets = (
            (None, {
                'fields': (
                    'email',
                    'description',
                )
            }),
            ('Advanced', {
                'fields': (
                    'id',
                    ('created_at', 'updated_at'),
                ),
                'classes': ('collapse','collapse-closed'),
            })
    )
    readonly_fields = (
                'email',
                'description',
                
                'id','created_at','updated_at',
    )

class PaymentAdmin( admin.ModelAdmin ):
    list_display = ('card_holder', 'last4', 'id', 'created_at')
    search_fields = ( 'card_holder', 'last4' )
    fieldsets = (
            (None, {
                'fields': (
                    ('client', 'type'),
                    ('card_type', 'last4'),
                    ('expire_month', 'expire_year'),
                    ('card_holder', 'country'),
                )
            }),
            ('Advanced', {
                'fields': (
                    'id',
                    ('created_at', 'updated_at'),
                ),
                'classes': ('collapse','collapse-closed'),
            })
    )
    readonly_fields = (
                'type',
                'card_type', 'last4',
                'expire_month', 'expire_year',
                'card_holder', 'country',
                
                'id', 'client', 'created_at', 'updated_at',
    )

class OfferAdmin( admin.ModelAdmin ):
    
    list_display = ('name', 'slug', 'amount', 'currency', 'interval', 'id', 'created_at')
    search_fields = ( 'name', )
    fieldsets = (
            (None, {
                'fields': (
                    ( 'name', 'slug' ),
                    ('amount', 'currency'),
                    ('interval', 'trial_period_days'),
                )
            }),
            ('Advanced', {
                'fields': (
                    'id',
                    ('created_at', 'updated_at'),
                ),
                'classes': ('collapse','collapse-closed'),
            })
    )
    readonly_fields = ( 'id', 'slug', 'created_at', 'updated_at', )

class TransactionAdmin( admin.ModelAdmin ):
    list_filter = ( 'status', 'refunded' )
    list_display = ( 'payment', 'status', 'origin_amount', 'currency', 'refunded' )
    exclude = ( 'livemode', 'amount', 'client' )
    actions = ['refund']
    fieldsets = (
            (None, {
                'fields': (
                    ('status', 'response_code'),
                    ('origin_amount', 'currency'),
                    'payment','description',

                )
            }),
            ('Refund', {
                'fields': (
                    ('refunded','refunded_at'),
                )
            }),
            ('Advanced', {
                'fields': (
                    'id',
                    ('created_at', 'updated_at'),
                ),
                'classes': ('collapse','collapse-closed'),
            })
    )
    readonly_fields = ( 
                        'status', 
                        'response_code', 
                        'origin_amount',
                        'currency',
                        'payment',
                        'description', 
                        'refunded', 'refunded_at',

                        'id', 'created_at', 'updated_at',                        
                    )

    def refund( self, request, queryset ):
        p = pymill.Pymill( settings.PAYMILL_PRIVATE_KEY )
        refunded = 0
        for transaction in queryset:
            refund = p.refund( transaction.id, transaction.origin_amount )['data']
            if refund['response_code'] == 20000:
                transaction.refunded = True
                transaction.refunded_at = datetime.utcfromtimestamp( refund['created_at'] )
                transaction.save()
                refunded += 1
        message = "1 transaction was" if refunded == 1 else "%s transactions were" % refunded
        self.message_user(request, "%s successfully refunded" % message)	
    refund.short_description = 'Refund transaction'

admin.site.register( Transaction, TransactionAdmin )
admin.site.register( Client, ClientAdmin )
admin.site.register( Payment, PaymentAdmin )
admin.site.register( Offer, OfferAdmin )
admin.site.register( Subscription )
