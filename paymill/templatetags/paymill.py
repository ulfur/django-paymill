#encoding: utf-8

from django import template
from django.conf import settings

from ..forms import PaymillForm

register = template.Library()
paymill_next = getattr( settings, 'PAYMILL_SUCCESS', '/' )

@register.inclusion_tag('paymill/form.html')
def paymill_form( amount, currency='USD', description='', next=paymill_next ):

    return {
        'paymill_key': settings.PAYMILL_PUBLIC_KEY,
        'paymill_form': PaymillForm( ),
        'amount': amount,
        'currency': currency,
        'next':next,
        'description':description,
    }
