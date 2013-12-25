#encoding: utf-8

from django.conf.urls import patterns, include, url

from .views import PaymillTransactionView, PaymillAddCardView

urlpatterns = patterns('',
    url(r'^transaction$',  PaymillTransactionView.as_view(), name='paymill-payment' ),
    url(r'^addcard$',  PaymillAddCardView.as_view(), name='paymill-add-card' ),
)
