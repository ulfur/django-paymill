#encoding: utf-8

WEBHOOK_EVENTS = (
    ('chargeback.executed','chargeback.executed'),              #returns a transaction-object with state set to chargeback

    ('transaction.created','transaction.created'),              #returns a transaction-object
    ('transaction.succeeded','transaction.succeeded'),          #returns a transaction-object
    ('transaction.failed','transaction.failed'),                #returns a transaction-object

    ('subscription.created','subscription.created'),            #returns a subscription-object
    ('subscription.updated','subscription.updated'),            #returns a subscription-object
    ('subscription.deleted','subscription.deleted'),            #returns a subscription-object
    ('subscription.succeeded','subscription.succeeded'),        #returns a transaction-object and a subscription-object
    ('subscription.failed','subscription.failed'),              #returns a transaction-object and a subscription-object

    ('refund.created','refund.created'),                        #returns a refund-object
    ('refund.succeeded','refund.succeeded'),                    #returns a refunds-object
    ('refund.failed','refund.failed'),                          #returns a refunds-object

    ('app.merchant.activated','app.merchant.activated'),        #returns a merchant-object if a connected merchant was activated
    ('app.merchant.deactivated','app.merchant.deactivated'),    #returns a merchant-object if a connected merchant was deactivated
    ('app.merchant.rejected','app.merchant.rejected'),          #returns a merchant-object if a connected merchant was rejected
    ('app.merchant.app.disabled','app.merchant.app.disabled'),  #returns a merchant object if a connected merchant disabled your app

    ('payout.transferred','payout.transferred'),                #returns an invoice-object with the payout sum for the invoice period
    ('invoice.available','invoice.available'),                  #returns an invoice-object with the fees sum for the invoice period
    ('client.updated','client.updated'),                        #returns a client-object if a client was updated
)

INTERVAL_CHOICES = (
    ('1 DAY','Daily'),
    ('1 WEEK','Weekly'),
    ('2 WEEK','Bimonthly'),
    ('1 MONTH','Monthly'),
    ('3 MONTH','Quarterly'),
    ('6 MONTH','Biannual'),
    ('1 YEAR','Annual'),
)

CURRENCY_CHOICES = (
    ('EUR', 'Euro'),
    ('USD', 'US Dollar'),
    ('GBP', 'Pound'),
)