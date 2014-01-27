VERSION = 0.1
def get_version():
    return VERSION

try:    
    from .webhooks import init_webhook
    def validate_webhook( secret ):
        return secret == WEBHOOK_SECRET
    WEBHOOK_SECRET = init_webhook( )
except:
    WEBHOOK_SECRET = None