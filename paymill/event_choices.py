#encoding: utf-8

WEBHOOK_EVENTS = (
    ('chargeback.executed', 'chargeback.executed'), 
    ('transaction.created','transaction.created'),
    ('transaction.succeeded','transaction.succeeded'),
    ('transaction.failed','transaction.failed'),
    ('subscription.created','subscription.created'),
    ('subscription.updated','subscription.updated'),
    ('subscription.deleted','subscription.deleted'),
    ('subscription.succeeded','subscription.succeeded'),
    ('subscription.failed','subscription.failed'),
    ('refund.created','refund.created'),
    ('refund.succeeded','refund.succeeded'),
    ('refund.failed','refund.failed'),
)