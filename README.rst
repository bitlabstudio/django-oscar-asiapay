AsiaPay package for django-oscar
================================

Payment integration of AsiaPay's PayDollar.


Installation
------------

Prerequisites:

* Django
* django-oscar

If you want to install the latest stable release from PyPi::

    $ pip install django-oscar-asiapay

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-oscar-asiapay.git#egg=asiapay

Add ``django-oscar-asiapay`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'oscar',
        'asiapay',
    )

Run the South migrations::

    ./manage.py migrate asiapay


Usage
-----

TODO

Settings
--------

ASIAPAY_PAYDOLLAR_URL
+++++++++++++++++++++

URL to connect to AsiaPay. Testing url::

    https://test.paydollar.com/b2cDemo/eng/payment/payForm.jsp

Production url::

    https://www.paydollar.com/b2c2/eng/payment/payForm.jsp


ASIAPAY_CURRENCY_CODE
+++++++++++++++++++++

Default: '702'

Currency you want to use. Please check the PayDollar Integration Guide.

ASIAPAY_LANGUAGE
++++++++++++++++

Default: 'E'

Language of the payment page.

- 'C': Traditional Chinese
- 'E': English
- 'F': French
- 'G': German
- 'J': Japanese
- 'R': Russian
- 'S': Spanish
- 'T': Thai
- 'V': Vietnamese
- 'X': Simplified Chinese

ASIAPAY_LOCALTEST_URL
+++++++++++++++++++++

Use this setting to test a response from AsiaPay locally. We can recommend
``ngrok`` to mask localhost.

ASIAPAY_CALLBACK_HTTPS
++++++++++++++++++++++

Default: True

Use ``https`` (True) or ``http`` (False) to construct reponse urls.

ASIAPAY_PAYTYPE
+++++++++++++++

Default: 'N'

Paytype you want to use. Please check the PayDollar Integration Guide.


Roadmap
-------

Check the issue tracker on github for milestones and features to come.
