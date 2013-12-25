#encoding: utf-8

from django import forms
from django.forms.util import flatatt
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.conf import settings

from datetime import datetime
today = datetime.now()

MONTHS = [ ('%02i'%i, '%02i'%i) for i in range(1,13) ]
YEARS  = [ ('%i'%i, '%i'%i) for i in range(today.year,today.year+11) ]

labels = getattr( settings, 'PAYMILL_LABELS', {} )

#An input field with no 'name' attribute prevents it from being passed to the server
class NameLess( forms.TextInput ):	
    def render( self, name, value, attrs=None ):
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        return format_html('<input{0} />', flatatt(final_attrs))

class PaymillForm( forms.Form ):

    cardnumber = forms.CharField(
                            label = _(labels.get( 'card_number', 'Card number' )),
                            max_length=16, 
                            widget=NameLess( attrs={ 'class':'card-number rem','size':'16', 'placeholder':'**** **** **** ****'} )
                        )

    expiry_month = forms.ChoiceField( 
                            label = _(labels.get( 'expiry_month', 'Expiry month' )),
                            choices=MONTHS,
                            widget=forms.Select( attrs={ 'class':'card-expiry-month rem'} )
                        )

    expiry_year = forms.ChoiceField( 
                            label = _(labels.get( 'expiry_year', 'Expiry year' )),
                            choices=YEARS,
                            widget=forms.Select( attrs={ 'class':'card-expiry-year rem'} )
                        )

    cvc = forms.CharField( 
                            label = _(labels.get( 'card_cvc', 'CVC' )),
                            max_length=3, 
                            widget=NameLess( attrs={ 'class':'card-cvc rem', 'size':'3', 'placeholder':'***'} )
                        )

    name = forms.CharField( 
                            label = _(labels.get( 'card_name', 'Name on card' )),
                            max_length=50,
                            widget=forms.TextInput( attrs={ 'class':'card-holdername' } )
                        )