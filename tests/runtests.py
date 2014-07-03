#!/usr/bin/env python
import sys
from coverage import coverage
from optparse import OptionParser

from django.conf import settings

if not settings.configured:
    extra_settings = {
        'ASIAPAY_PAYDOLLAR_URL': 'https://www.sandbox.asiapay.com/webscr',
        'ASIAPAY_SANDBOX_MODE': True,
        'ASIAPAY_VERSION': '88.0',
    }
    # To specify integration settings (which include passwords, hence why they
    # are not committed), create an integration.py module.
    try:
        from integration import *
    except ImportError:
        extra_settings.update({
            'ASIAPAY_API_USERNAME': '',
            'ASIAPAY_API_PASSWORD': '',
            'ASIAPAY_API_SIGNATURE': '',
        })
    else:
        for key, value in locals().items():
            if key.startswith('ASIAPAY'):
                extra_settings[key] = value

    from oscar.defaults import *
    for key, value in locals().items():
        if key.startswith('OSCAR'):
            extra_settings[key] = value
    extra_settings['OSCAR_ALLOW_ANON_CHECKOUT'] = True

    from oscar import get_core_apps, OSCAR_MAIN_TEMPLATE_DIR

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.flatpages',
            'django.contrib.staticfiles',
            'asiapay',
            'compressor',
            'south',
        ] + get_core_apps(),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.transaction.TransactionMiddleware',
            'oscar.apps.basket.middleware.BasketMiddleware',
        ),
        TEMPLATE_CONTEXT_PROCESSORS = (
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.request",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "django.contrib.messages.context_processors.messages",
            # Oscar specific
            'oscar.apps.search.context_processors.search_form',
            'oscar.apps.promotions.context_processors.promotions',
            'oscar.apps.checkout.context_processors.checkout',
            'oscar.core.context_processors.metadata',
            'oscar.apps.customer.notifications.context_processors.notifications',
        ),
        DEBUG=False,
        SOUTH_TESTS_MIGRATE=False,
        HAYSTACK_CONNECTIONS={
            'default': {
                'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
            },
        },
        TEMPLATE_DIRS=(OSCAR_MAIN_TEMPLATE_DIR,),
        SITE_ID=1,
        ROOT_URLCONF='tests.urls',
        COMPRESS_ENABLED=False,
        STATIC_URL='/',
        STATIC_ROOT='/static/',
        NOSE_ARGS=['-s', '--with-spec'],
        **extra_settings
    )

from django_nose import NoseTestSuiteRunner


def run_tests(*test_args):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    c = coverage(source=['asiapay'], omit=['*migrations*', '*tests*'],
                 auto_data=True)
    c.start()
    num_failures = test_runner.run_tests(test_args)
    c.stop()

    if num_failures > 0:
        sys.exit(num_failures)
    print "Generating HTML coverage report"
    c.html_report()


def generate_migration():
    from south.management.commands.schemamigration import Command
    com = Command()
    com.handle(app='asiapay', initial=True)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)