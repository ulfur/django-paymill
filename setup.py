#encoding: utf-8
from setuptools import setup, find_packages
from paymill import get_version

setup(
    name = "django-paymill",
    version = get_version(),
    description = "django-paymill is a django app for easily integrating Paymill as a payment gateway for django projects.",
    author = "Úlfur Kristjánsson",
    author_email = "ulfurk@ulfurk.com",
    url = "https://github.com/ulfur/django-paymill",
    packages = find_packages( ),
    include_package_data=True,
    classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
        ],
    install_requires=['django >= 1.6', 'django-crispy-forms', 'pymill']
)
