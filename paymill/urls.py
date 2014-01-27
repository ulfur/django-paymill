#encoding: utf-8

from django.conf.urls import patterns, include, url

from .views import PaymillTransactionView, PaymillAddCardView, WebhookView

urlpatterns = patterns('',
    url( r'^transaction$',  PaymillTransactionView.as_view( ), name='paymill-payment' ),
    url( r'^addcard$',  PaymillAddCardView.as_view( ), name='paymill-add-card' ),
#    url( r'^webhooks$',  WebhookView.as_view( ), name='paymill-webhook' ),
    url( r'^webhook/(?P<secret>\w{32})$',  WebhookView.as_view( ), name='paymill-webhook' ),
)
