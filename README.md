django-paymill
==============

django-paymill is a django app for easily integrating Paymill as a payment gateway for django projects.

django-paymill requires [pymill](https://github.com/kliment/pymill) and as a resulting dependency [Requests](http://docs.python-requests.org/en/latest/)

django-paymill also requires, for the time being, [django-crispy-forms](https://github.com/maraujop/django-crispy-forms)

Simply install the app and the requirements and add them to your INSTALLED_APPS:

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    
        'crispy_forms',
        'paymill',
    )

Then add your Paymill public and private keys to settings:

    PAYMILL_PRIVATE_KEY = ''
    PAYMILL_PUBLIC_KEY = ''

For webhooks to work you will need to declare the receiving host:

    PAYMILL_WEBHOOK_HOST = ''

And off you go! :)

(More documentation to follow soon)
