import django.dispatch

subscription_created    = django.dispatch.Signal( providing_args=('event',) ),
subscription_updated    = django.dispatch.Signal( providing_args=('event',) ),
subscription_deleted    = django.dispatch.Signal( providing_args=('event',) ),
subscription_succeeded  = django.dispatch.Signal( providing_args=('event',) ),
subscription_failed     = django.dispatch.Signal( providing_args=('event',) ),

