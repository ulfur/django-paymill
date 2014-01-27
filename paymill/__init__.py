
from .webhooks import init_webhook

def validate_webhook( secret ):
    return secret == WEBHOOK_SECRET
WEBHOOK_SECRET = init_webhook( )