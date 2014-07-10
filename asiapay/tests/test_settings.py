"""Settings that need to be set in order to run the tests."""
import logging
import os

from oscar import get_core_apps
from oscar.defaults import *  # NOQA


ASIAPAY_PAYDOLLAR_URL = "ASIAPAY_URL"
ASIAPAY_MERCHANT_ID = "12345"

logging.getLogger('factory').setLevel(logging.WARN)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

DEBUG = True
FILER_DEBUG = True

SITE_ID = 1

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

USE_I18N = True

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
)

ROOT_URLCONF = 'asiapay.tests.urls'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../../static/')
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../../media/')

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'test_static'),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../templates'),
)

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), 'coverage')

COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_nose',
    'oscar',
] + get_core_apps()

INTERNAL_APPS = [
    'asiapay',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS

SECRET_KEY = 'foobar'
