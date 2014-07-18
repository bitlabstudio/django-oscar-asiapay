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

Hook this app into your ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^asiapay/', include('asiapay.urls')),
    )

Run the South migrations::

    ./manage.py migrate asiapay


Usage
-----

Please make sure you have installed ``django-oscar`` (up and running).
You can easily customize oscar by overwriting its apps. Please check oscar's
docs if you don't know what I'm talking about.

To use AsiaPay please check the directory ``oscar_integration_example``.

Basically the ``OscarPaymentDetailsView`` has been overwritten, so the user
will be re-directed to AsiaPay after confirming the checkout. We've customized
the ``preview.html`` template::

	<form method="post" action="{{ asiapay_url }}">
		{% csrf_token %}
		<input type="hidden" name="merchantId" value="{{ merchant_id }}">
		<input type="hidden" name="currCode" value="{{ currency_code }}">
		<input type="hidden" name="orderRef" value="{{ order_number }}">
		<input type="hidden" name="amount" value="{{ order_total.incl_tax }}">
		<input type="hidden" name="successUrl" value="{{ success_url }}">
		<input type="hidden" name="failUrl" value="{{ fail_url }}">
		<input type="hidden" name="errorUrl" value="{{ error_url }}">
		<input type="hidden" name="lang" value="{{ asiapay_lang }}">
		<input type="hidden" name="payType" value="{{ asiapay_paytype }}">
		<img src="https://raw.githubusercontent.com/bitmazk/django-oscar-asiapay/master/payv_logo.gif" alt="{% trans "AsiaPay" %}" />
		<button id='place-order' type="submit" class="btn btn-primary btn-block js-disable-on-click" data-loading-text="{% trans "Sending..." %}">{% trans "Submit" %}</button>
	</form>

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


ASIAPAY_SUCCESS_REDIRECT
++++++++++++++++++++++++

Default: reverse('checkout:thank-you')

URL to redirect to after successful transaction. Use for example::

    ASIAPAY_SUCCESS_REDIRECT = '/'

or::

    ASIAPAY_SUCCESS_REDIRECT = reverse_lazy('your_url_name')


ASIAPAY_FAILURE_REDIRECT
++++++++++++++++++++++++

Default: reverse('basket:summary')

URL to redirect to after failed transaction. Use for example::

    ASIAPAY_SUCCESS_REDIRECT = '/'

or::

    ASIAPAY_SUCCESS_REDIRECT = reverse_lazy('your_url_name')


Roadmap
-------

Check the issue tracker on github for milestones and features to come.
