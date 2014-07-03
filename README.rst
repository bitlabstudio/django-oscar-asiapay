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


Roadmap
-------

Check the issue tracker on github for milestones and features to come.
