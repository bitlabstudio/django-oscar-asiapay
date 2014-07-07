import os
from setuptools import setup, find_packages
import asiapay


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

install_requires = [
    'django',
    'django-oscar',
    'django-localflavor',
    'requests>=1.0',
]

tests_require = [
    'django_libs',
    'fabric',
    'factory_boy',
    'django-nose',
    'coverage',
    'django-coverage',
    'mock',
]

setup(
    name="django-oscar-asiapay",
    version=asiapay.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, oscar, payment, paydollar, asiapay',
    author='Tobias Lorenz',
    author_email='tobias.lorenz@bitmazk.com',
    url="https://github.com/bitmazk/django-oscar-asiapay",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='asiapay.tests.runtests.runtests',
)
